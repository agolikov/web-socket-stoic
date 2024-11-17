# Stoic Wisdom Web App

This is a simple web application that delivers Stoic wisdom phrases to the user in real-time through WebSockets. Users can pin their favorite phrases and view the pinned list.

## Features

- Random Stoic phrases delivered every 30 seconds.
- Real-time updates using WebSockets.
- Pin favorite phrases and view the pinned list.
- Easy setup with Docker.

## Prerequisites

- Docker and Docker Compose installed on your machine.

## How to Run

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. Build and start the containers:

    ```bash
    docker-compose up --build
    ```

3. Open your browser:
    - **Frontend**: [http://localhost:8080](http://localhost:8080)
    - **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

4. Enjoy Stoic wisdom!

## Stopping the Application

To stop the containers:

```bash
docker-compose down
```

## Customization

- Modify `backend.py` to change the Stoic phrases or add new features.
- Update `index.html` for frontend changes.

## Future Improvements

- Add persistent storage for pinned phrases.
- Implement user accounts for personalized experience.
- Deploy to a cloud platform.