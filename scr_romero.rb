require 'open-uri'
require 'nokogiri'
require 'csv'

class Extractor
  def initialize
    @base_url = "https://news.ycombinator.com/"
    @headers = {
      "User-Agent" => "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    }
    @nombre_archivo = "data/romero.csv"
  end

  def iniciar_archivo
    CSV.open(@nombre_archivo, 'w') do |csv|
      csv << %w[Pagina Titulo Sitio Puntos Comentarios Relevancia]
    end
  end 

  def guardar(datos)
    CSV.open(@nombre_archivo, 'a') do |csv|
      csv << datos
    end
  end

  def procesar_paginas(total_paginas)
    iniciar_archivo

    (1..total_paginas).each do |num_pag|

      link_actual = "#{@base_url}?p=#{num_pag}"

      puts "\n--------------------------------------------------"
      puts "📡 Conectando a Página #{num_pag} de #{total_paginas}."
      puts "🔗 URL: #{link_actual}"

      begin
        html = URI.open(link_actual, @headers)
      rescue OpenURI::HTTPError => e
        puts "Error al abrir la página #{num_pag}: #{e.message}"
        next
      end

      datos = html.read
      doc = Nokogiri::HTML(datos)

      filas_noticias = doc.css('tr.athing')

      filas_noticias.each do |fila_titulo|

        elemento_titulo = fila_titulo.css('.titleline > a').first
        titulo = elemento_titulo ? elemento_titulo.inner_text.strip : "Sin titulo"

        elemento_sitio = fila_titulo.css('.sitebit a span.sitestr').first
        sitio = elemento_sitio ? elemento_sitio.inner_text.strip : "Desconocido"
        
        fila_meta = fila_titulo.next_element

        elemento_puntos = fila_meta.css('.score').first
        puntos = elemento_puntos ? elemento_puntos.inner_text.gsub(' points', '').strip : "0"

        links_meta = fila_meta.css('a')
        link_comentarios = links_meta.find { |a| a.inner_text.include?('comments') }
        comentarios = link_comentarios ? link_comentarios.inner_text.gsub(' comments', '').strip : "0"

        titulo_low = titulo.downcase
        if titulo_low.match?(/(ai|gpt|llm|model|data|intelligence|robot|python|neural|machine learning)/)
          relevancia = "ALTA (IA)"
        else
          relevancia = "General Tech"
        end

        guardar([num_pag, titulo, sitio, puntos, comentarios, relevancia])
      end

      puts "Página #{num_pag} completada."

      if num_pag < total_paginas
        sleep(1) 
      end
    end

    puts "\nScraping Finalizado con éxito."
  end
end


extractor = Extractor.new
paginas = 0

loop do
  print "\n¿Cuántas páginas de Hacker News desea analizar? (Min 1 - Max 10): "
  input = gets.chomp

  if input.match?(/^\d+$/)
    paginas = input.to_i
    if paginas >= 1 && paginas <= 10
      break
    else
      puts "Por favor, ingresa un número entre 1 y 10."
    end
  else
    puts "Entrada inválida. Ingresa solo números."
  end
end

extractor.procesar_paginas(paginas)
