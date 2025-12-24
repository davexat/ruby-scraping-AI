require 'open-uri'
require 'nokogiri'
require 'csv'

# --- CONFIGURACIÓN ---
url_portada = 'https://arstechnica.com/ai/'

# OpenURI necesita los headers para simular un navegador real
headers = {
  'User-Agent' => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

puts 'Conectando a la portada con OpenURI...'

begin
  # 1. ABRIR PORTADA
  html_portada = URI.open(url_portada, headers)
  doc = Nokogiri::HTML(html_portada)

  articulos = doc.css('article')
  puts "Se encontraron #{articulos.count} noticias. Comenzando extracción..."

  CSV.open('noticias_ars_openuri.csv', 'wb') do |csv|
    csv << ['Titulo', 'Link', 'Contenido Completo']

    articulos.each_with_index do |articulo, index|
      # --- Extracción de Título y Link ---
      nodo_titulo = articulo.at_css('h2 a') || articulo.at_css('header a')

      next unless nodo_titulo # Saltar si no hay título

      titulo = nodo_titulo.text.strip
      link = nodo_titulo['href']

      puts "\n[#{index + 1}/#{articulos.count}] Procesando: #{titulo[0..30]}..."

      # --- Extracción Profunda (Entrar al Link) ---
      begin
        # Pausa de cortesía (Vital para OpenURI también)
        sleep 1

        # 2. ABRIR DETALLE
        html_detalle = URI.open(link, headers)
        doc_detalle = Nokogiri::HTML(html_detalle)

        # Buscamos el contenido en las clases típicas de Ars Technica
        nodos_texto = doc_detalle.css('.post-content p, .article-content p, div[itemprop="articleBody"] p')

        # Limpieza y unión de párrafos
        contenido = nodos_texto.map { |p| p.text.strip }.reject(&:empty?).join("\n\n")

        contenido = 'Contenido multimedia o estructura no reconocida.' if contenido.empty?

        csv << [titulo, link, contenido]
        puts "Texto extraído (#{contenido.length} caracteres)."
      rescue OpenURI::HTTPError => e
        # Captura errores como 404 Not Found o 403 Forbidden
        puts "Error HTTP al entrar al link: #{e.message}"
        csv << [titulo, link, "Error HTTP: #{e.message}"]
      rescue StandardError => e
        # Captura otros errores (conexión, timeouts)
        puts "Error general: #{e.message}"
        csv << [titulo, link, "Error: #{e.message}"]
      end
    end
  end

  puts "\nFin del Scraping. Guardado en 'jaren.csv'."
rescue OpenURI::HTTPError => e
  puts "Error fatal al abrir la portada: #{e.message}"
end
