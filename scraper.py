import requests
from bs4 import BeautifulSoup
import os

KALRO_URL = "https://www.kalro.org/information-resources/information-brochures/"

def get_pdf_links():
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(KALRO_URL, headers=headers)


    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        pdf_links = []

        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.endswith(".pdf"):
                if not href.startswith("http"):  # Convert relative links to absolute
                    href = KALRO_URL + href
                pdf_links.append(href)

        return pdf_links
    else:
        return []
print(response.text)

def download_pdfs():
    pdf_links = get_pdf_links()
    if not pdf_links:
        print("⚠️ No PDFs found. Check if the website structure has changed.")
        return

    os.makedirs("kalro_pdfs", exist_ok=True)

    for pdf in pdf_links:
        pdf_name = pdf.split("/")[-1]
        pdf_path = os.path.join("kalro_pdfs", pdf_name)

        try:
            response = requests.get(pdf, stream=True)
            response.raise_for_status()  # Raise error for failed requests

            with open(pdf_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            print(f"✅ Downloaded: {pdf_name}")

        except requests.exceptions.RequestException as e:
            print(f"⚠️ Failed to download {pdf_name}: {e}")

if __name__ == "__main__":
    download_pdfs()
