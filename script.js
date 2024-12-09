document.addEventListener('DOMContentLoaded', () => {
    const sendLocationButton = document.getElementById('send-location-button');
    const sendAlertButton = document.getElementById('send-alert-button');
    const submitDetailsButton = document.getElementById('submit-details-button');
    const messageElement = document.getElementById('message');
    const addressElement = document.getElementById('address');
    const departmentSection = document.getElementById('department-section');
    const extraInfoSection = document.getElementById('extra-info');
    const departmentImagesSection = document.getElementById('department-images');

    let address = '';

    sendLocationButton.addEventListener('click', sendLocation);
    sendAlertButton.addEventListener('click', sendAlert);
    submitDetailsButton.addEventListener('click', sendDetails);

    function sendLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const { latitude, longitude } = position.coords;
                    messageElement.textContent = `Location sent: Latitude = ${latitude}, Longitude = ${longitude}`;
                    
                    // Simulating address fetch
                    address = '123 Emergency St, Danger City, 12345';
                    addressElement.textContent = `Address: ${address}`;

                    sendLocationButton.classList.add('hidden');
                    departmentSection.classList.remove('hidden');
                },
                (error) => {
                    messageElement.textContent = `Error getting location: ${error.message}`;
                }
            );
        } else {
            messageElement.textContent = 'Geolocation is not supported by this browser.';
        }
    }

    function sendAlert() {
        const selectedDepartments = Array.from(document.querySelectorAll('#department-list input[type=checkbox]:checked'))
            .map(checkbox => checkbox.value);

        if (selectedDepartments.length === 0) {
            alert('Please select at least one department.');
            return;
        }

        messageElement.textContent = `Alert sent to ${selectedDepartments.join(', ')}`;
        
        const departmentImages = {
            ambulance: 'https://placeholder.co/150x150?text=Ambulance',
            firefighter: 'https://placeholder.co/150x150?text=Firefighter',
            rescue: 'https://placeholder.co/150x150?text=Rescue',
            police: 'https://placeholder.co/150x150?text=Police'
        };

        departmentImagesSection.innerHTML = '';
        selectedDepartments.forEach(department => {
            const img = document.createElement('img');
            img.src = departmentImages[department];
            img.alt = `${department.charAt(0).toUpperCase() + department.slice(1)} Image`;
            departmentImagesSection.appendChild(img);
        });

        departmentImagesSection.classList.remove('hidden');
        departmentSection.classList.add('hidden');
        extraInfoSection.classList.remove('hidden');
    }

    function sendDetails() {
        const userName = document.getElementById('user-name').value;
        const problemDetails = document.getElementById('problem-details').value;

        if (!userName || !problemDetails) {
            alert('Please fill in all fields.');
            return;
        }

        messageElement.textContent = 'Details submitted successfully.';
        extraInfoSection.classList.add('hidden');
    }
});
