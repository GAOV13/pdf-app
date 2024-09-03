document.addEventListener('DOMContentLoaded', function() {
    const documentLinks = document.querySelectorAll('.document-link');
    const previewFrame = document.getElementById('preview-frame');

    documentLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const description = this.getAttribute('data-description');
            const url = this.getAttribute('data-url');
            const descriptionContainer = this.parentElement.querySelector('.description-container');
            const descriptionText = descriptionContainer.querySelector('.description-text');

            // Hide all other descriptions
            document.querySelectorAll('.description-container').forEach(container => {
                container.style.display = 'none';
            });

            // Show the selected description
            descriptionText.textContent = description;
            descriptionContainer.style.display = 'block';
        });
    });
});