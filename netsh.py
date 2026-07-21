import subprocess
import ctypes
import sys
from typing import List, Dict, Optional

# TODO: handle WPA3-Enterprise or 802.1x profiles where key is not exportable this way

def get_oem_encoding() -> str:
    try:
        # Windows console commands like netsh output in the active OEM code page
        cp = ctypes.windll.kernel32.GetOEMCP()
        if cp:
            return f"cp{cp}"
    except Exception:
        pass
    return sys.getdefaultencoding() or "utf-8"

def run_netsh(args: List[str]) -> str:
    encoding = get_oem_encoding()
    # print(f"DEBUG: decoding netsh output using: {encoding}")
    res = subprocess.run(
        ["netsh"] + args,
        capture_output=True,
        check=False
    )
    return res.stdout.decode(encoding, errors="replace")

def get_wifi_profiles() -> List[str]:
    output = run_netsh(["wlan", "show", "profiles"])
    profiles = []
    
    # Non-English systems translate "All User Profile". We match typical localized variations
    # by checking for common fragments of the word "profile" or "user".
    profile_keywords = {"profile", "profil", "perfil", "профиль", "utente", "user"}
    
    for line in output.splitlines():
        if ":" not in line:
            continue
        left, right = line.split(":", 1)
        left_lower = left.lower()
        if any(kw in left_lower for kw in profile_keywords):
            name = right.strip()
            if name:
                profiles.append(name)
    return profiles

def get_profile_details(profile_name: str) -> Dict[str, Optional[str]]:
    output = run_netsh(["wlan", "show", "profile", f"name={profile_name}", "key=clear"])
    
    details = {
        "ssid": profile_name,
        "authentication": None,
        "cipher": None,
        "password": None
    }
    
    # Common translations of key fields in localized Windows setups
    key_content_keywords = {
        "key content", "contenido de la clave", "schlüsselinhalt",
        "contenu de la clé", "contenuto chiave", "conteúdo da chave",
        "содержимое ключа", "treść klucza", "key-content", "nyckelinnehåll",
        "sleutelinhoud"
    }
    
    auth_keywords = {"authentication", "autenticación", "authentifizierung", "authentification", "autenticazione", "autenticação", "аутентификация", "uwierzytelnianie"}
    cipher_keywords = {"cipher", "cifrado", "verschlüsselung", "chiffrement", "cifrario", "criptografia", "шифр", "szyfr"}
    
    for line in output.splitlines():
        if ":" not in line:
            continue
        left, right = line.split(":", 1)
        left_clean = left.strip().lower()
        val_clean = right.strip()
        
        if left_clean in key_content_keywords:
            details["password"] = val_clean
        elif any(kw in left_clean for kw in auth_keywords):
            details["authentication"] = val_clean
        elif any(kw in left_clean for kw in cipher_keywords):
            details["cipher"] = val_clean
            
    return details
