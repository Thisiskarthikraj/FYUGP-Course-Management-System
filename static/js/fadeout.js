
        // Show the welcome message for 30 seconds
        setTimeout(function() {
            var welcomeMessage = document.getElementById('welcome-message');
            var subsequentMessage = document.getElementById('subsequent-message');
            
            // Fade out the welcome message
            welcomeMessage.classList.add('fade-out');
            
            // After the welcome message fades out, show the subsequent message
            setTimeout(function() {
                welcomeMessage.classList.add('d-none');
                subsequentMessage.classList.remove('d-none');
            }, 3000); // Time to wait before showing subsequent message (3 seconds)
        }, 3000); // Time to display the welcome message (30 seconds)
