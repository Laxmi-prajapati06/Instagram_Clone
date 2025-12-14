document.addEventListener('DOMContentLoaded', function() {
    setupLikeButtons();

    setupCommentForms();
    
    setupImageUpload();
    
    setupModals();
    
    setupFollowButtons();
});

function setupLikeButtons() {
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('like-btn') || e.target.closest('.like-btn')) {
            const likeBtn = e.target.classList.contains('like-btn') ? e.target : e.target.closest('.like-btn');
            const postId = likeBtn.dataset.postId;
            const likeCount = document.querySelector(`.like-count-${postId}`);
            
            const isLiked = likeBtn.textContent.includes('Liked');
            const newLikedState = !isLiked;
            
            if (newLikedState) {
                likeBtn.innerHTML = '❤️ Liked';
                likeBtn.style.color = '#ed4956';
            } else {
                likeBtn.innerHTML = '🤍 Like';
                likeBtn.style.color = '#262626';
            }
            
            fetch(`/like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (likeCount) {
                    likeCount.textContent = `${data.likes_count} likes`;
                }
            })
            .catch(error => {
                console.error('Error liking post:', error);
                if (newLikedState) {
                    likeBtn.innerHTML = '🤍 Like';
                    likeBtn.style.color = '#262626';
                } else {
                    likeBtn.innerHTML = '❤️ Liked';
                    likeBtn.style.color = '#ed4956';
                }
            });
        }
    });
}

function setupCommentForms() {
    document.querySelectorAll('.comment-form').forEach(form => {
        const input = form.querySelector('.comment-input');
        const submitBtn = form.querySelector('.comment-submit');
        
        if (input && submitBtn) {
            input.addEventListener('input', function() {
                submitBtn.disabled = this.value.trim() === '';
            });
        }
    });
}

function setupImageUpload() {
    const uploadArea = document.querySelector('.upload-area');
    const fileInput = document.querySelector('#image-upload');
    const imagePreview = document.querySelector('.image-preview');
    const removeImageBtn = document.querySelector('.remove-image');
    
    if (uploadArea && fileInput) {
        uploadArea.addEventListener('click', () => fileInput.click());
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('drag-over');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('drag-over');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('drag-over');
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                handleFileSelect(e.dataTransfer.files[0]);
            }
        });
        
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length) {
                handleFileSelect(e.target.files[0]);
            }
        });
    }
    
    if (removeImageBtn) {
        removeImageBtn.addEventListener('click', () => {
            if (fileInput) fileInput.value = '';
            if (imagePreview) imagePreview.style.display = 'none';
            if (removeImageBtn) removeImageBtn.style.display = 'none';
            if (uploadArea) uploadArea.style.display = 'block';
        });
    }
    
    function handleFileSelect(file) {
        if (!file.type.match('image.*')) {
            alert('Please select an image file.');
            return;
        }
        
        const reader = new FileReader();
        reader.onload = function(e) {
            if (imagePreview) {
                imagePreview.src = e.target.result;
                imagePreview.style.display = 'block';
            }
            if (uploadArea) uploadArea.style.display = 'none';
            if (removeImageBtn) removeImageBtn.style.display = 'inline';
        };
        reader.readAsDataURL(file);
    }
}

function setupModals() {
    document.querySelectorAll('[data-modal]').forEach(btn => {
        btn.addEventListener('click', () => {
            const modalId = btn.dataset.modal;
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.style.display = 'flex';
                document.body.style.overflow = 'hidden';
            }
        });
    });

    document.querySelectorAll('.modal-close, .modal-overlay').forEach(el => {
        el.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal-close') || 
                e.target.classList.contains('modal-overlay')) {
                const modal = e.target.closest('.modal-overlay');
                if (modal) {
                    modal.style.display = 'none';
                    document.body.style.overflow = 'auto';
                }
            }
        });
    });
}

function setupFollowButtons() {
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('follow-btn') || e.target.closest('.follow-btn')) {
            const followBtn = e.target.classList.contains('follow-btn') ? e.target : e.target.closest('.follow-btn');
            const userId = followBtn.dataset.userId;
            
            if (!userId) return;
            
            const isFollowing = followBtn.textContent.includes('Following');
            followBtn.disabled = true;
            followBtn.innerHTML = isFollowing ? 'Follow' : 'Following';
            followBtn.classList.toggle('btn-secondary', !isFollowing);
            
            fetch(`/follow/${userId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
            })
            .catch(error => {
                console.error('Error following user:', error);
                followBtn.disabled = false;
                followBtn.innerHTML = isFollowing ? 'Following' : 'Follow';
                followBtn.classList.toggle('btn-secondary', isFollowing);
            });
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showLoading(message = 'Loading...') {
    const loadingOverlay = document.createElement('div');
    loadingOverlay.className = 'loading-overlay';
    loadingOverlay.innerHTML = `
        <div class="spinner"></div>
        <div class="loading-text">${message}</div>
    `;
    document.body.appendChild(loadingOverlay);
}

function hideLoading() {
    const loadingOverlay = document.querySelector('.loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.remove();
    }
}