from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

def get_video_info(url):
    # Instagram App User-Agent (Taaki server ko lage mobile app se request aayi hai)
    mobile_user_agent = 'Instagram 219.0.0.12.117 Android (30/11; 320dpi; 1080x1920; samsung; SM-G960F; starlte; samsungexynos9810; en_US; 273667793)'
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'geo_bypass': True,
        'nocheckcertificate': True,
        'extract_flat': False, # Pura data extract karo
        
        # Yahan humne "Samsung Phone" wali ID lagayi hai
        'http_headers': {
            'User-Agent': mobile_user_agent,
            'Accept': '*/*',
            'Accept-Language': 'en-US',
            'Sec-Fetch-Mode': 'navigate',
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Video info extract karo
            info = ydl.extract_info(url, download=False)
            
            return {
                "status": "success",
                "title": info.get('title', 'Instagram Reel'),
                "thumbnail": info.get('thumbnail'),
                "download_url": info.get('url')
            }
    except Exception as e:
        error_msg = str(e)
        # Agar fir bhi error aaye, toh user ko saaf batao
        if "Login required" in error_msg or "rate-limit" in error_msg:
            return {
                "status": "error", 
                "message": "Instagram Security High hai. Server IP Blocked. Please try YouTube/Twitter link."
            }
        return {"status": "error", "message": "Link expire ho gaya hai ya private hai."}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-video', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"status": "error", "message": "Link kahan hai?"})
    
    result = get_video_info(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)    
    result = get_video_info(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
