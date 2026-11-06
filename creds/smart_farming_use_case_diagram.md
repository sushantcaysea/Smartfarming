# Use Case Diagram Specification: Smart Farming Decision Support System

This document outlines the **UML Use Case Diagram** for the **Smart Farming Decision Support System**. It highlights the system boundary, the two main actors (Farmer/User and Administrator), and the core use cases including precision crop recommendations (via RF & SVM) and computer vision leaf diagnostics.

---

## 1. Visual Use Case Diagram

Below is the custom-generated visual Use Case Diagram designed for your Smart Farming system:

![Smart Farming Use Case Diagram](file:///C:/Users/Asus/.gemini/antigravity/brain/754f73f0-fb3e-4e4a-b75a-26a97ff5b3c8/smart_farming_usecase_1780209215370.png)

---

## 2. Interactive & Editable UML Diagram (Mermaid)

The following diagram is generated using Mermaid. It offers a live, interactive, color-coded view of the relationships, including system boundaries, actors, and specific dependencies.

```mermaid
graph LR
    %% Styles and Classes
    classDef actor fill:#e1f5fe,stroke:#0288d1,stroke-width:2px,rx:10px,color:#01579b,font-weight:bold;
    classDef usecase fill:#e8f5e9,stroke:#2e7d32,stroke-width:1.5px,rx:20px,color:#1b5e20;
    classDef system fill:#fafafa,stroke:#37474f,stroke-width:3px,stroke-dasharray: 5 5,color:#263238,font-weight:bold;

    subgraph UserSpace [" "]
        Farmer["👨‍🌾 Farmer / User"]:::actor
    end

    subgraph SystemBoundary ["Smart Farming System Boundary"]
        UC_Signup["Signup"]:::usecase
        UC_Register["Register"]:::usecase
        UC_Login["Login"]:::usecase
        
        UC_Input["Input Soil & Climatic Parameters<br/>(N, P, K, pH, Temp, Hum, Rainfall)"]:::usecase
        UC_PredictCrop["Get Crop Recommendation<br/>(Compare RF vs. SVM)"]:::usecase
        UC_UploadLeaf["Upload Leaf Image"]:::usecase
        UC_Diagnose["Diagnose Plant Disease<br/>(Custom CNN Pathology)"]:::usecase
        
        UC_ManageUsers["Manage Users"]:::usecase
        UC_Retrain["Retrain Crop Models<br/>(RF / SVM)"]:::usecase
        UC_Monitor["Monitor Diagnostic Logs"]:::usecase
    end

    subgraph AdminSpace [" "]
        Admin["💻 Administrator"]:::actor
    end

    %% Farmer Connections
    Farmer --> UC_Register
    Farmer --> UC_Login
    Farmer --> UC_Input
    Farmer --> UC_UploadLeaf

    %% Relationships
    UC_Register -.->|"<<extends>>"| UC_Signup
    UC_Login -.->|"<<includes>>"| UC_Input
    UC_Input -.->|"<<includes>>"| UC_PredictCrop
    UC_UploadLeaf -.->|"<<includes>>"| UC_Diagnose

    %% Administrator Connections
    Admin --> UC_ManageUsers
    Admin --> UC_Retrain
    Admin --> UC_Monitor

    %% Stylings
    style SystemBoundary fill:#f9fbe7,stroke:#827717,stroke-width:2px;
    style UserSpace fill:none,stroke:none;
    style AdminSpace fill:none,stroke:none;
```

---

## 3. Structural Comparison & Mapping

Below is a tabular mapping comparing your baseline "House Price Prediction System" with the new **"Smart Farming Decision Support System"**:

| Component | House Price Prediction System | Smart Farming Decision Support System |
| :--- | :--- | :--- |
| **Primary Actor** | User | **Farmer / User** (End-user seeking agricultural guidance) |
| **Secondary Actor**| Admin | **Administrator** (Manages users, monitors logs, updates weights) |
| **Core Inputs** | Location, Size, Amenities | **Soil Properties** (N, P, K, pH) & **Climatic Parameters** (Temp, Humidity, Rainfall) |
| **Key Use Cases** | `Input values`, `Prediction` | `Input Soil & Climatic Parameters`, `Get Crop Recommendation` (RF/SVM dual compare), `Upload Leaf Image` |
| **Specialized Extensions**| N/A | `Diagnose Plant Disease` (via deep-learning CNN leaf pathology) |
| **Admin Operations** | `Manage Users`, `Retrain Model`, `Monitor Predictions` | `Manage Users`, `Retrain Recommendation Models`, `Monitor Diagnostic Logs` |

---

## 4. Key Relationships & Rationale

* **`Register` extends `Signup`**: Enables basic sign-up and authentication procedures.
* **`Login` includes `Input Parameters`**: Accessing recommendations requires a logged-in session, ensuring profile history and farm diagnostics are linked to the correct user.
* **`Input Parameters` includes `Get Crop Recommendation`**: Once soil and microclimatic parameters are logged, the system feeds these directly into the dual-stage **Random Forest** and **Support Vector Machine (SVM)** inference pipelines to generate top-5 recommendations.
* **`Upload Leaf Image` includes `Diagnose Plant Disease`**: Dragging/dropping leaf samples triggers the deep-learning backend to run standard ImageNet verification (MobileNetV2) and output diagnostic classifications.
