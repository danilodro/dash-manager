import streamlit as st
import security

def setup_page(page_title):
    st.set_page_config(
        page_title=page_title,
        page_icon="🪐",
    )

    if st.experimental_get_query_params().get('code'):
        security.handle_redirect()

    access_token = st.session_state.get('access_token')

    if access_token:
        user_info = security.get_user_info(access_token)
        st.session_state['user_info'] = user_info
        return True
    else:
        # Centralizando e aumentando o texto
        st.markdown("<h2 style='text-align: center; font-size: 24px;'>Please sign-in to use this app.</h2>", unsafe_allow_html=True)

        # Adicionando a imagem
        image_url = "https://botminio.apps.intelbras.com.br/redes/intel-dash.png"
        st.image(image_url, use_column_width=True)

        # Adicionando o botão "Sign In"
        auth_url = security.get_auth_url()
        st.markdown(f"<p style='text-align: center;'><a href='{auth_url}' target='_self' class='streamlit-button button-primary' style='background-color: #00a75d; color: white; padding: 0.375rem 0.75rem; border-radius: 0.25rem;'>Sign in to Azure</a></p>", unsafe_allow_html=True)

        st.stop()
