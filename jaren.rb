require 'httparty'
require 'nokogiri'
require 'csv'

# --- CONFIGURACIÓN ---
url_portada = 'https://arstechnica.com/ai/'
headers = {
  'User-Agent' => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

puts "📡 Conectando a la portada: #{url_portada}..."
response = HTTParty.get(url_portada, headers: headers)

if response.code == 200
  doc = Nokogiri::HTML(response.body)
  articulos = doc.css('article')

  puts "🔍 Se encontraron #{articulos.count} noticias. Comenzando extracción profunda..."

  CSV.open('noticias_completas_ars.csv', 'wb') do |csv|
    # Encabezados del CSV
    csv << ['Titulo', 'Link', 'Contenido Completo']

    articulos.each_with_index do |articulo, index|
      # 1. Obtener datos básicos de la portada
      nodo_titulo = articulo.at_css('h2 a') || articulo.at_css('header a')

      next unless nodo_titulo # Si no hay título, saltamos

      titulo = nodo_titulo.text.strip
      link = nodo_titulo['href']

      puts "\n[#{index + 1}/#{articulos.count}] Procesando: #{titulo[0..30]}..."
      puts '   ↳ Accediendo al link...'

      # 2. ENTRAR A LA NOTICIA (Segunda Petición)
      begin
        response_detalle = HTTParty.get(link, headers: headers)

        if response_detalle.code == 200
          doc_detalle = Nokogiri::HTML(response_detalle.body)

          # 3. EXTRAER CONTENIDO COMPLETO
          # Ars Technica pone el texto en divs con clase 'post-content' o 'article-content'
          # Buscamos todos los párrafos <p> dentro de esas clases.
          nodos_texto = doc_detalle.css('.post-content p, .article-content p, div[itemprop="articleBody"] p')

          # Unimos todos los párrafos con un salto de línea, limpiando espacios
          contenido_completo = nodos_texto.map { |p| p.text.strip }.reject(&:empty?).join("\n\n")

          # Si por alguna razón no encuentra texto (ej: es un video), ponemos un aviso
          contenido_completo = 'No se pudo extraer el texto o es contenido multimedia.' if contenido_completo.empty?

          # 4. GUARDAR EN CSV
          csv << [titulo, link, contenido_completo]
          puts "   ✅ Contenido extraído (#{contenido_completo.length} caracteres)."

        else
          puts "   ❌ Error al entrar al link (Código #{response_detalle.code})"
          csv << [titulo, link, 'Error de acceso']
        end
      rescue StandardError => e
        puts "   ❌ Error de conexión: #{e.message}"
        csv << [titulo, link, "Error: #{e.message}"]
      end

      # 5. PAUSA DE CORTESÍA (Evita bloqueos)
      sleep 1
    end
  end

  puts "\n🎉 ¡Misión cumplida! Revisa el archivo 'noticias_completas_ars.csv'."

else
  puts "❌ Error al conectar con la portada: Código #{response.code}"
end
