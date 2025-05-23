# Pulsur Project

Pulsur aims to help cities and transport agencies better understand citizens' mobility perceptions and behaviors, whether they use public transport or not. It bridges the gap between service supply and lived experience, enabling targeted interventions to increase ridership, revenue, and achieve sustainability goals.

This repository contains the codebase for the Pulsur project, which is structured into several distinct applications:

*   **`/identity`**: Manages user authentication, registration, and access control for the Pulsur platform. It handles secure login, role differentiation (Admin, Client/User), and ensures that only authorized users can access the system.
*   **`/interface`**: Provides the main user-facing dashboards and tools for clients. It allows users to visualize persona mapping, analyze trends, and access actionable insights. It also includes an IAM section for client-side user management.
*   **`/admin`**: The central administration interface for Pulsur administrators. It allows for the management of all client data, system settings, user accounts (from `/identity`), and overall platform oversight.
*   **`/finance`**: Handles all financial aspects of the Pulsur application, including subscription management, billing, and payment processing.

Each application is designed to be a standalone service with its own database and API for communication with other services, ensuring a modular and scalable architecture.

Further details for each application, including setup and configuration, can be found in their respective `README.md` files.
