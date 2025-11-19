"""Streamlit frontend application."""
import streamlit as st
import requests
from datetime import datetime
from typing import Optional

# API base URL
API_BASE_URL = "http://localhost:8888"

# Initialize session state
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "login"


def login(email: str, password: str) -> bool:
    """Login user and store access token."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/jwt/login",
            data={"username": email, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.access_token = data.get("access_token")
            # Get user info
            user_response = requests.get(
                f"{API_BASE_URL}/users/me",
                headers={"Authorization": f"Bearer {st.session_state.access_token}"}
            )
            if user_response.status_code == 200:
                st.session_state.user = user_response.json()
            return True
        else:
            st.error(f"Login failed: {response.json().get('detail', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return False


def register(email: str, password: str) -> bool:
    """Register new user."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json={"email": email, "password": password}
        )
        if response.status_code == 201:
            st.success("Registration successful! Please login.")
            return True
        else:
            error_detail = response.json().get('detail', {})
            if isinstance(error_detail, dict):
                error_msg = error_detail.get('msg', 'Unknown error')
            else:
                error_msg = str(error_detail)
            st.error(f"Registration failed: {error_msg}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return False


def get_headers() -> dict:
    """Get headers with authentication token."""
    if st.session_state.access_token:
        return {"Authorization": f"Bearer {st.session_state.access_token}"}
    return {}


def get_feed() -> Optional[dict]:
    """Get feed posts."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/feed",
            headers=get_headers()
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to load feed: {response.json().get('detail', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None


def upload_file(file, caption: str) -> bool:
    """Upload image/video file."""
    try:
        files = {"file": (file.name, file, file.type)}
        data = {"caption": caption}
        response = requests.post(
            f"{API_BASE_URL}/upload",
            files=files,
            data=data,
            headers=get_headers()
        )
        if response.status_code == 200:
            st.success("File uploaded successfully!")
            return True
        else:
            st.error(f"Upload failed: {response.json().get('detail', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")
        return False


def delete_post(post_id: str) -> bool:
    """Delete a post."""
    try:
        response = requests.delete(
            f"{API_BASE_URL}/post/{post_id}",
            headers=get_headers()
        )
        if response.status_code == 200:
            st.success("Post deleted successfully!")
            return True
        else:
            st.error(f"Delete failed: {response.json().get('detail', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"Error deleting post: {str(e)}")
        return False


def format_datetime(dt_str: str) -> str:
    """Format datetime string for display."""
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return dt_str


def main():
    """Main application entry point."""
    st.set_page_config(page_title="Image Feed", page_icon="📸", layout="wide")

    # Sidebar for navigation
    if st.session_state.access_token:
        with st.sidebar:
            user_email = st.session_state.user.get('email', 'Unknown') if st.session_state.user else 'Unknown'
            st.write(f"**Logged in as:** {user_email}")
            if st.button("Logout"):
                st.session_state.access_token = None
                st.session_state.user = None
                st.session_state.page = "login"
                st.rerun()

    # Login/Register page
    if not st.session_state.access_token:
        st.title("📸 Image Feed")

        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            st.header("Login")
            with st.form("login_form"):
                email = st.text_input("Email", key="login_email")
                password = st.text_input("Password", type="password", key="login_password")
                submit = st.form_submit_button("Login")

                if submit:
                    if login(email, password):
                        st.rerun()

        with tab2:
            st.header("Register")
            with st.form("register_form"):
                email = st.text_input("Email", key="register_email")
                password = st.text_input("Password", type="password", key="register_password")
                submit = st.form_submit_button("Register")

                if submit:
                    if register(email, password):
                        st.rerun()

    # Main feed page
    else:
        st.title("📸 Image Feed")

        # Upload section
        with st.expander("📤 Upload New Post", expanded=False):
            uploaded_file = st.file_uploader(
                "Choose an image or video file",
                type=['png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'],
                key="upload_file"
            )
            caption = st.text_area("Caption", key="upload_caption", placeholder="Write a caption...")

            if st.button("Upload", key="upload_button"):
                if uploaded_file:
                    if upload_file(uploaded_file, caption):
                        st.rerun()
                else:
                    st.warning("Please select a file to upload")

        st.divider()

        # Feed section
        st.header("Feed")

        feed_data = get_feed()

        if feed_data and feed_data.get("posts"):
            posts = feed_data["posts"]

            if not posts:
                st.info("No posts yet. Be the first to upload!")
            else:
                for post in posts:
                    with st.container():
                        col1, col2 = st.columns([0.9, 0.1])

                        with col1:
                            st.write(f"**{post.get('email', 'Unknown')}**")
                            st.caption(f"Posted on {format_datetime(post.get('created_at', ''))}")

                        with col2:
                            if post.get("is_owner", False):
                                if st.button("🗑️", key=f"delete_{post['id']}", help="Delete post"):
                                    if delete_post(post['id']):
                                        st.rerun()

                        # Display image or video
                        url = post.get("url", "")
                        file_type = post.get("file_type", "image")

                        if url:
                            if file_type == "video":
                                st.video(url)
                            else:
                                st.image(url, use_container_width=True)

                        # Display caption
                        caption = post.get("caption", "")
                        if caption:
                            st.write(caption)

                        st.divider()
        else:
            st.info("Loading feed...")


if __name__ == "__main__":
    main()

