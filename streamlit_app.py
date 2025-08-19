import streamlit as st
import argostranslate.package
import argostranslate.translate
import os
import time
from typing import List, Dict, Tuple

# Page configuration
st.set_page_config(
    page_title="Argos Translate",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .translation-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin: 10px 0;
    }
    .language-info {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 10px 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'installed_packages' not in st.session_state:
    st.session_state.installed_packages = []
if 'available_packages' not in st.session_state:
    st.session_state.available_packages = []
if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []

@st.cache_data
def get_language_mapping() -> Dict[str, str]:
    """Map language codes to full names"""
    return {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French', 
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'zh': 'Chinese',
        'ja': 'Japanese',
        'ko': 'Korean',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'nl': 'Dutch',
        'sv': 'Swedish',
        'da': 'Danish',
        'no': 'Norwegian',
        'fi': 'Finnish',
        'pl': 'Polish',
        'cs': 'Czech',
        'sk': 'Slovak',
        'hu': 'Hungarian',
        'tr': 'Turkish',
        'uk': 'Ukrainian',
        'he': 'Hebrew',
        'th': 'Thai',
        'vi': 'Vietnamese',
        'id': 'Indonesian',
        'ms': 'Malay',
        'tl': 'Filipino',
        'fa': 'Persian',
        'ur': 'Urdu',
        'bn': 'Bengali',
        'te': 'Telugu',
        'ta': 'Tamil',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'gu': 'Gujarati',
        'pa': 'Punjabi',
        'or': 'Odia',
        'as': 'Assamese',
        'ne': 'Nepali',
        'si': 'Sinhala',
        'my': 'Myanmar',
        'km': 'Khmer',
        'lo': 'Lao',
        'ka': 'Georgian',
        'am': 'Amharic',
        'sw': 'Swahili',
        'zu': 'Zulu',
        'af': 'Afrikaans',
        'is': 'Icelandic',
        'mt': 'Maltese',
        'cy': 'Welsh',
        'ga': 'Irish',
        'eu': 'Basque',
        'ca': 'Catalan',
        'gl': 'Galician',
        'eo': 'Esperanto'
    }

def refresh_installed_packages():
    """Refresh the list of installed language packages"""
    try:
        installed_languages = argostranslate.translate.get_installed_languages()
        st.session_state.installed_packages = []
        
        for lang in installed_languages:
            translations = lang.translations_from
            for translation in translations:
                package_info = {
                    'from_code': lang.code,
                    'from_name': lang.name,
                    'to_code': translation.to_lang.code,
                    'to_name': translation.to_lang.name
                }
                st.session_state.installed_packages.append(package_info)
    except Exception as e:
        st.error(f"Error refreshing installed packages: {str(e)}")

def refresh_available_packages():
    """Refresh the list of available packages from the repository"""
    try:
        with st.spinner("Updating package index..."):
            argostranslate.package.update_package_index()
            available_packages = argostranslate.package.get_available_packages()
            
            st.session_state.available_packages = []
            for package in available_packages:
                package_info = {
                    'from_code': package.from_code,
                    'from_name': package.from_name,
                    'to_code': package.to_code,
                    'to_name': package.to_name,
                    'package': package
                }
                st.session_state.available_packages.append(package_info)
    except Exception as e:
        st.error(f"Error updating package index: {str(e)}")

def install_package(package_info):
    """Install a translation package"""
    try:
        with st.spinner(f"Installing {package_info['from_name']} → {package_info['to_name']}..."):
            download_path = package_info['package'].download()
            argostranslate.package.install_from_path(download_path)
            return True
    except Exception as e:
        st.error(f"Error installing package: {str(e)}")
        return False

def translate_text(text: str, from_code: str, to_code: str) -> str:
    """Translate text from one language to another"""
    try:
        translated_text = argostranslate.translate.translate(text, from_code, to_code)
        return translated_text
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return ""

def get_available_language_pairs() -> List[Tuple[str, str, str, str]]:
    """Get list of available translation pairs from installed packages"""
    refresh_installed_packages()
    return [(pkg['from_code'], pkg['from_name'], pkg['to_code'], pkg['to_name']) 
            for pkg in st.session_state.installed_packages]

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🌐 Argos Translate</h1>', unsafe_allow_html=True)
    st.markdown("**Open-source offline neural machine translation**")
    
    # Sidebar for package management
    with st.sidebar:
        st.header("📦 Package Management")
        
        # Refresh buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh Installed", use_container_width=True):
                refresh_installed_packages()
                st.success("Refreshed!")
        
        with col2:
            if st.button("📥 Update Index", use_container_width=True):
                refresh_available_packages()
                st.success("Updated!")
        
        # Show installed packages
        st.subheader("Installed Packages")
        if not st.session_state.installed_packages:
            refresh_installed_packages()
        
        if st.session_state.installed_packages:
            for pkg in st.session_state.installed_packages[:10]:  # Show first 10
                st.markdown(f"✅ **{pkg['from_name']}** → **{pkg['to_name']}**")
        else:
            st.info("No packages installed yet. Install some below!")
        
        # Package installation
        st.subheader("Install New Packages")
        
        if st.button("📡 Load Available Packages", use_container_width=True):
            refresh_available_packages()
        
        if st.session_state.available_packages:
            # Create a list of package options for selection
            package_options = []
            for pkg in st.session_state.available_packages:
                option = f"{pkg['from_name']} → {pkg['to_name']}"
                package_options.append(option)
            
            if package_options:
                selected_package = st.selectbox(
                    "Select package to install:",
                    options=range(len(package_options)),
                    format_func=lambda x: package_options[x],
                    key="package_selector"
                )
                
                if st.button("📥 Install Selected Package", use_container_width=True):
                    pkg_to_install = st.session_state.available_packages[selected_package]
                    if install_package(pkg_to_install):
                        st.success(f"Successfully installed {pkg_to_install['from_name']} → {pkg_to_install['to_name']}")
                        refresh_installed_packages()
                        st.rerun()
        
        # Quick install popular packages
        st.subheader("Quick Install")
        popular_pairs = [
            ("en", "es", "English → Spanish"),
            ("en", "fr", "English → French"), 
            ("en", "de", "English → German"),
            ("es", "en", "Spanish → English"),
            ("fr", "en", "French → English"),
            ("de", "en", "German → English")
        ]
        
        for from_code, to_code, display_name in popular_pairs:
            if st.button(f"📥 {display_name}", use_container_width=True, key=f"quick_{from_code}_{to_code}"):
                # Find the package in available packages
                for pkg in st.session_state.available_packages:
                    if pkg['from_code'] == from_code and pkg['to_code'] == to_code:
                        if install_package(pkg):
                            st.success(f"Installed {display_name}")
                            refresh_installed_packages()
                            st.rerun()
                        break
    
    # Main translation interface
    available_pairs = get_available_language_pairs()
    language_mapping = get_language_mapping()
    
    if not available_pairs:
        st.warning("⚠️ No translation packages installed! Please install some packages from the sidebar.")
        st.info("💡 **Getting Started:**\n1. Click 'Load Available Packages' in the sidebar\n2. Select and install a language pair\n3. Start translating!")
        return
    
    # Create language selection interface
    st.subheader("🔤 Select Languages")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**From Language:**")
        from_languages = sorted(list(set([(pair[0], pair[1]) for pair in available_pairs])))
        from_options = [f"{lang[1]} ({lang[0]})" for lang in from_languages]
        
        selected_from_idx = st.selectbox(
            "Source language:",
            range(len(from_options)),
            format_func=lambda x: from_options[x],
            key="from_lang"
        )
        selected_from_code = from_languages[selected_from_idx][0]
    
    with col2:
        st.markdown("**To Language:**")
        # Filter available target languages based on selected source
        to_languages = sorted([(pair[2], pair[3]) for pair in available_pairs if pair[0] == selected_from_code])
        to_options = [f"{lang[1]} ({lang[0]})" for lang in to_languages]
        
        if to_options:
            selected_to_idx = st.selectbox(
                "Target language:",
                range(len(to_options)),
                format_func=lambda x: to_options[x],
                key="to_lang"
            )
            selected_to_code = to_languages[selected_to_idx][0]
        else:
            st.error("No target languages available for the selected source language.")
            return
    
    # Translation interface
    st.subheader("✍️ Translation")
    
    # Input text
    input_text = st.text_area(
        f"Enter text in {from_languages[selected_from_idx][1]}:",
        height=150,
        placeholder="Type your text here...",
        key="input_text"
    )
    
    # Translation controls
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        translate_button = st.button("🚀 Translate", type="primary", use_container_width=True)
    
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_button:
        st.session_state.input_text = ""
        st.rerun()
    
    # Perform translation
    if translate_button and input_text.strip():
        with st.spinner("Translating..."):
            translated_text = translate_text(input_text, selected_from_code, selected_to_code)
            
            if translated_text:
                # Display translation
                st.subheader("📝 Translation Result")
                st.markdown(f'<div class="translation-box"><h4>🎯 {to_languages[selected_to_idx][1]}:</h4><p style="font-size: 1.1em; line-height: 1.5;">{translated_text}</p></div>', unsafe_allow_html=True)
                
                # Add to history
                translation_record = {
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                    'from_lang': from_languages[selected_from_idx][1],
                    'to_lang': to_languages[selected_to_idx][1],
                    'original': input_text,
                    'translated': translated_text
                }
                st.session_state.translation_history.insert(0, translation_record)
                
                # Keep only last 10 translations
                st.session_state.translation_history = st.session_state.translation_history[:10]
                
                # Copy button
                st.code(translated_text, language=None)
    
    elif translate_button and not input_text.strip():
        st.error("Please enter some text to translate.")
    
    # Translation history
    if st.session_state.translation_history:
        st.subheader("📚 Recent Translations")
        
        for i, record in enumerate(st.session_state.translation_history[:5]):
            with st.expander(f"{record['from_lang']} → {record['to_lang']} ({record['timestamp']})"):
                st.markdown(f"**Original ({record['from_lang']}):**")
                st.write(record['original'])
                st.markdown(f"**Translation ({record['to_lang']}):**")
                st.write(record['translated'])
    
    # Footer
    st.markdown("---")
    st.markdown("**About Argos Translate:** Open-source offline neural machine translation powered by OpenNMT")
    st.markdown("🔗 [GitHub](https://github.com/argosopentech/argos-translate) | 📖 [Documentation](https://argos-translate.readthedocs.io/)")

if __name__ == "__main__":
    main()