from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

def get_video_info(url):
    # Instagram ko dhoka dene ke liye Fake Browser Headers
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'geo_bypass': True,
        'nocheckcertificate': True,
        # Yahan hum bata rahe hain ki hum Windows PC se aaye hain
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # download=False server par load kam karne ke liye
            info = ydl.extract_info(url, download=False)
            
            return {
                "status": "success",
                "title": info.get('title', 'Video Download'),
                "thumbnail": info.get('thumbnail'),
                "download_url": info.get('url')
            }
    except Exception as e:
        # Agar error aaye to clean message bhejo
        error_msg = str(e)
        if "Login required" in error_msg:
            return {"status": "error", "message": "Instagram ne server IP block kiya hai. Kripya dusri video try karein."}
        return {"status": "error", "message": error_msg}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-video', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"status": "error", "message": "No URL provided"})
    
    result = get_video_info(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
@app.route('/get-video', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"status": "error", "message": "No URL provided"})
    
    result = get_video_info(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
