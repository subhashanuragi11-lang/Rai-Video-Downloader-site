from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

def get_video_info(url):
    # Render par FFmpeg nahi hota, isliye hum 'best' format
    # wo mangenge jisme Audio+Video pehle se mixed ho.
    ydl_opts = {
        'format': 'best[ext=mp4]/best',  # MP4 format prefer karo
        'quiet': True,
        'no_warnings': True,
        'geo_bypass': True,
        'nocheckcertificate': True,
        
        # Fake User-Agent (YouTube/Insta ko lagega PC hai)
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Info extract karo (Download False rakhna hai)
            info = ydl.extract_info(url, download=False)
            
            # YouTube Shorts kabhi-kabhi formats list mein hote hain
            download_url = info.get('url')
            
            # Agar direct URL nahi mila, to formats mein se dhundo
            if not download_url:
                formats = info.get('formats', [])
                for f in formats:
                    # Wo format dhundo jisme video aur audio dono ho (acodec != none)
                    if f.get('ext') == 'mp4' and f.get('acodec') != 'none':
                        download_url = f.get('url')
                        break
            
            return {
                "status": "success",
                "title": info.get('title', 'Video Download'),
                "thumbnail": info.get('thumbnail'),
                "download_url": download_url
            }
            
    except Exception as e:
        # Error ka asli reason user ko dikhao
        return {"status": "error", "message": str(e)}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-video', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"status": "error", "message": "Link missing!"})
    
    result = get_video_info(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
