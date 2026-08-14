"""
data_sync.py — Fetches latest packages & hotels from Spring Boot backend
and stores them as vector embeddings in ChromaDB so the chatbot always
has fresh, searchable data.
"""

import os
import requests
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain_community.embeddings import SentenceTransformerEmbeddings

load_dotenv()

SPRING_BOOT_URL = os.getenv("SPRING_BOOT_URL", "http://localhost:8080")
CHROMA_PATH = "./chroma_data"

# Reuse the same embedding model across calls
embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


def _fetch_packages() -> list[dict]:
    """Fetch all active packages from Spring Boot backend."""
    url = f"{SPRING_BOOT_URL}/api/packages/chatbot-data"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        print(f"[Sync] ✅ Fetched {len(data)} active packages from database")
        return data
    except requests.exceptions.ConnectionError:
        print(f"[Sync] ❌ Cannot reach backend at {SPRING_BOOT_URL} — is Spring Boot running?")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"[Sync] ❌ HTTP error fetching packages: {e}")
        return []
    except Exception as e:
        print(f"[Sync] ❌ Unexpected error fetching packages: {e}")
        return []


def _fetch_hotels() -> list[dict]:
    """Fetch all approved hotels from Spring Boot backend."""
    url = f"{SPRING_BOOT_URL}/api/hotels/chatbot-data"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        print(f"[Sync] ✅ Fetched {len(data)} approved hotels from database")
        return data
    except requests.exceptions.ConnectionError:
        print(f"[Sync] ❌ Cannot reach backend at {SPRING_BOOT_URL} — is Spring Boot running?")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"[Sync] ❌ HTTP error fetching hotels: {e}")
        return []
    except Exception as e:
        print(f"[Sync] ❌ Unexpected error fetching hotels: {e}")
        return []


def _build_package_document(pkg: dict) -> Document:
    """Convert a package dict into a LangChain Document for embedding."""
    price_from = pkg.get('priceFrom')
    price_to   = pkg.get('priceTo')
    adult_price = pkg.get('basePriceAdult')
    child_price = pkg.get('basePriceChild')

    if price_from and price_to:
        price_str = f"${price_from} – ${price_to} USD"
    elif price_from:
        price_str = f"From ${price_from} USD"
    elif price_to:
        price_str = f"Up to ${price_to} USD"
    else:
        price_str = "Contact agent for pricing"

    per_person = ""
    if adult_price:
        per_person = f"${adult_price} USD per adult"
        if child_price:
            per_person += f", ${child_price} USD per child"

    parts = [
        f"Travel Package: {pkg.get('packageName', 'Unknown Package')}",
        f"Package ID: {pkg.get('packageId', '')}",
        f"Description: {pkg.get('description', '')}",
        f"Destination: {pkg.get('destination', '')}",
        f"District: {pkg.get('district', '')}",
        f"Start Place: {pkg.get('startPlace', '')}",
        f"End Place: {pkg.get('endPlace', '')}",
        f"Duration: {pkg.get('duration', '')}",
        f"Price: {price_str}",
        f"Price Per Person: {per_person}",
        f"Inclusions: {pkg.get('inclusions', '')}",
        f"Category: {pkg.get('category', '')}",
        f"Travel Agent: {pkg.get('agentName', '')}",
        f"Rating: {pkg.get('rating', '')}",
        f"Trending: {'Yes' if pkg.get('trending') else 'No'}",
    ]
    # Filter out lines with empty values
    text = "\n".join(line for line in parts if not line.endswith(": ") and line.split(": ", 1)[-1].strip())
    metadata = {
        "type": "package",
        "id": str(pkg.get("id", "")),
        "name": str(pkg.get("packageName", "")),
        "district": str(pkg.get("district", "")),
    }
    return Document(page_content=text, metadata=metadata)


def _build_hotel_document(hotel: dict) -> Document:
    """Convert a hotel dict into a LangChain Document for embedding."""
    price_from = hotel.get('priceFrom')
    price_to   = hotel.get('priceTo')
    if price_from and price_to:
        price_str = f"${price_from} – ${price_to} USD per night"
    elif price_from:
        price_str = f"From ${price_from} USD per night"
    elif price_to:
        price_str = f"Up to ${price_to} USD per night"
    else:
        price_str = "Contact hotel for pricing"

    amenities = hotel.get('amenities', [])
    if isinstance(amenities, list):
        amenities_str = ", ".join(amenities) if amenities else ""
    else:
        amenities_str = str(amenities)

    parts = [
        f"Hotel: {hotel.get('hotelName', 'Unknown Hotel')}",
        f"Description: {hotel.get('description', '')}",
        f"Destination: {hotel.get('destination', '')}",
        f"Location: {hotel.get('location', '')}",
        f"District: {hotel.get('district', '')}",
        f"Price: {price_str}",
        f"Amenities: {amenities_str}",
    ]
    text = "\n".join(line for line in parts if not line.endswith(": ") and not line.endswith(": USD per night"))
    metadata = {
        "type": "hotel",
        "id": str(hotel.get("id", "")),
        "name": str(hotel.get("hotelName", "")),
    }
    return Document(page_content=text, metadata=metadata)


def sync_all_data():
    """
    Main sync function — fetches packages & hotels from backend,
    converts them to Documents, embeds them, and stores in ChromaDB.
    Called on startup, every 5 minutes (auto-sync), and via /notify-update.
    """
    print("[Sync] 🔄 Starting data sync with backend...")

    packages = _fetch_packages()
    hotels = _fetch_hotels()

    docs = []
    for pkg in packages:
        try:
            docs.append(_build_package_document(pkg))
        except Exception as e:
            print(f"[Sync] ⚠️  Skipping package due to error: {e}")

    for hotel in hotels:
        try:
            docs.append(_build_hotel_document(hotel))
        except Exception as e:
            print(f"[Sync] ⚠️  Skipping hotel due to error: {e}")

    print(f"[Sync] 📊 Total items to embed: {len(docs)} (packages + hotels)")

    if not docs:
        print("[Sync] ⚠️  No data to embed — ChromaDB will be empty. Backend might be starting up.")
        return

    try:
        # Wipe and rebuild so old data doesn't persist
        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=embedding_model,
            persist_directory=CHROMA_PATH,
            collection_name="travelhub_data",
        )
        vectorstore.persist()
        print(f"[Sync] ✅ SYNC COMPLETE! {len(docs)} items now in ChromaDB with latest database state")
        print("[Sync] Chatbot is ready to provide accurate recommendations based on current offerings")
    except Exception as e:
        print(f"[Sync] ❌ ChromaDB write error: {e}")


def load_vectorstore() -> Chroma:
    """Load the existing ChromaDB vectorstore for querying."""
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_model,
        collection_name="travelhub_data",
    )
