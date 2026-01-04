# DevconBackEnd
# Devcon '26 Registration Backend

A complete FastAPI backend system for managing Devcon '26 event registrations, payments, and team management.

## Features

- **User Authentication**: JWT-based authentication with role-based access control
- **Registration System**: Public registration with participant profiles
- **Payment Processing**: Online payment receipts and cash collection
- **Team Management**: Team creation and joining with unique codes
- **QR Code Generation**: Event entry QR codes for verified participants
- **Admin Dashboard**: Comprehensive management and reporting tools
- **Email Notifications**: Automated registration and payment confirmations

## User Roles

- **Participant**: Students registering for the event
- **Ambassador**: Campus ambassadors collecting cash payments
- **Registration Team**: Staff managing registrations
- **Admin**: Full system access and management

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Database**
   - Create PostgreSQL database named 'Devcon'
   - Update connection string in `app/config.py` if needed

3. **Start Server**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

4. **Access API Documentation**
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

### Public Endpoints
- `GET /api/v1/public/tracks` - Available competition tracks
- `GET /api/v1/public/universities` - Supported universities
- `GET /api/v1/public/stats` - Registration statistics
- `POST /api/v1/public/register` - Public registration

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Current user info

### Payments
- `POST /api/v1/payments/upload-receipt` - Upload payment receipt
- `POST /api/v1/payments/select-cash` - Select cash payment
- `GET /api/v1/payments/my-payment` - Payment status

### Ambassador
- `POST /api/v1/ambassador/search` - Search participants
- `POST /api/v1/ambassador/verify-cash/{id}` - Verify cash payment
- `GET /api/v1/ambassador/pending-cash` - Pending cash payments

### Admin
- `GET /api/v1/admin/dashboard` - Admin dashboard
- `POST /api/v1/admin/verify-online/{id}` - Verify online payment
- `GET /api/v1/admin/search` - Search payments
- `GET /api/v1/admin/export` - Export data

## Environment Variables

Create a `.env` file:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://postgres:1234@localhost:5432/Devcon
ACCESS_TOKEN_EXPIRE_MINUTES=30
REGISTRATION_FEE=500.0
```

## Database Schema

- **Users**: Authentication and basic information
- **Participants**: Student details and preferences
- **Teams**: Team formation and management
- **Payments**: Payment tracking and verification
- **Audit Logs**: System activity tracking

## Security

- bcrypt password hashing
- JWT token-based authentication
- Role-based access control
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy

## Tech Stack

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Database
- **Pydantic**: Data validation
- **JWT**: Authentication tokens
- **bcrypt**: Password hashing

## License

This project is licensed under the MIT License.
# Deviii
