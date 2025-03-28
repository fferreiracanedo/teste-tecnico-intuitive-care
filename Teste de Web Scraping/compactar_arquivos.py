import os
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile


url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


pdf_links = []
for link in soup.find_all('a', href=True):
    if 'anexo' in link['href'] and link['href'].endswith('.pdf'):
        pdf_links.append(link['href'])


pdf_files = []
for i, pdf_link in enumerate(pdf_links):
    pdf_response = requests.get(pdf_link)
    pdf_file = f'anexo_{i+1}.pdf'
    with open(pdf_file, 'wb') as f:
        f.write(pdf_response.content)
    pdf_files.append(pdf_file)

zip_filename = 'anexos.zip'
with ZipFile(zip_filename, 'w') as zipf:
    for pdf_file in pdf_files:
        zipf.write(pdf_file)
        os.remove(pdf_file)