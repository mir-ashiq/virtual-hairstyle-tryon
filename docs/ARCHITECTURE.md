# Architecture Documentation

## System Overview

The Virtual Hairstyle Try-On application follows a modern, enterprise-level architecture with clear separation of concerns and modular design.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Gradio UI Layer                      │
│                    (app_enhanced.py)                    │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Service Layer                          │
│  ┌──────────────────────┐  ┌──────────────────────┐   │
│  │ HairstyleTransfer    │  │ HairstyleGallery     │   │
│  │ Service              │  │ Service              │   │
│  └──────────┬───────────┘  └──────────┬───────────┘   │
└─────────────┼──────────────────────────┼───────────────┘
              │                          │
┌─────────────▼──────────────────────────▼───────────────┐
│                   Model Layer                           │
│  ┌──────────────────────┐  ┌──────────────────────┐   │
│  │ BarbershopModel      │  │ BaseModel            │   │
│  │ (StyleGAN2)          │  │ (Abstract)           │   │
│  └──────────────────────┘  └──────────────────────┘   │
└─────────────┬───────────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────────┐
│                 Utility Layer                            │
│  ┌─────────────┐  ┌────────────┐  ┌─────────────┐      │
│  │ImageValidator│  │ImageProc   │  │Logger       │      │
│  └─────────────┘  └────────────┘  └─────────────┘      │
└─────────────┬───────────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────────┐
│            Configuration Layer                           │
│                  (settings.py)                           │
└──────────────────────────────────────────────────────────┘
```

## Layer Descriptions

### 1. UI Layer (Presentation)

**Files**: `app.py`, `app_enhanced.py`

**Responsibilities**:
- User interface rendering
- Input collection
- Result display
- User interaction handling

**Technologies**:
- Gradio 4.16.0
- Custom CSS styling
- Progressive disclosure UI patterns

### 2. Service Layer (Business Logic)

**Files**: `src/services/*.py`

**Components**:

#### HairstyleTransferService
- Orchestrates the hairstyle transfer process
- Manages validation and preprocessing
- Coordinates between models and utilities
- Provides high-level API for transfers

#### HairstyleGalleryService
- Manages hairstyle collections
- Organizes samples by category
- Provides gallery browsing
- Handles sample metadata

**Responsibilities**:
- Business logic execution
- Workflow orchestration
- Data validation
- Error handling
- Progress tracking

### 3. Model Layer (AI/ML)

**Files**: `src/models/*.py`

**Components**:

#### BaseModel (Abstract)
- Defines model interface
- Common model operations
- Validation methods
- Cleanup procedures

#### BarbershopModel
- StyleGAN2-based implementation
- Face alignment processing
- Hairstyle transfer execution
- Model state management

**Responsibilities**:
- AI model integration
- Model initialization
- Inference execution
- Model resource management

### 4. Utility Layer (Cross-cutting)

**Files**: `src/utils/*.py`

**Components**:

#### ImageValidator
- File validation
- Content validation
- Size/format checking
- Quality thresholds

#### ImageProcessor
- Resize operations
- Enhancement filters
- Color conversion
- Cropping utilities

#### Logger
- Structured logging
- Log file management
- Console output
- Error tracking

**Responsibilities**:
- Reusable utilities
- Common operations
- Helper functions
- Validation logic

### 5. Configuration Layer

**Files**: `src/config/*.py`

**Responsibilities**:
- Centralized configuration
- Environment variable handling
- Path management
- Feature flags
- Default values

## Data Flow

### Hairstyle Transfer Flow

```
1. User uploads images → UI Layer
2. UI calls transfer_service.transfer_hairstyle()
3. Service validates inputs → ImageValidator
4. Service preprocesses images → ImageProcessor
5. Service calls model.process()
6. Model performs face alignment
7. Model executes StyleGAN2 transfer
8. Model returns result
9. Service post-processes result
10. UI displays result to user
```

### Gallery Browsing Flow

```
1. User selects category → UI Layer
2. UI calls gallery_service.get_hairstyles_by_category()
3. Service reads from file system
4. Service returns hairstyle list
5. UI displays gallery
6. User selects hairstyle
7. UI loads selected image
```

## Design Patterns

### 1. Singleton Pattern
- **Where**: Settings configuration
- **Why**: Single source of truth for configuration
- **Implementation**: `get_settings()` function

### 2. Service Layer Pattern
- **Where**: Business logic layer
- **Why**: Separation of concerns, testability
- **Implementation**: `HairstyleTransferService`, `HairstyleGalleryService`

### 3. Template Method Pattern
- **Where**: Base model class
- **Why**: Define algorithm structure, allow customization
- **Implementation**: `BaseModel` abstract class

### 4. Facade Pattern
- **Where**: Service layer
- **Why**: Simplify complex subsystems
- **Implementation**: Services hide complexity of models/utils

### 5. Strategy Pattern
- **Where**: Transfer styles (realistic vs fidelity)
- **Why**: Interchangeable algorithms
- **Implementation**: Style parameter in model

## Key Principles

### 1. Separation of Concerns
- Each layer has distinct responsibilities
- No cross-layer dependencies except through interfaces
- Clear boundaries between components

### 2. Dependency Inversion
- High-level modules don't depend on low-level modules
- Both depend on abstractions (BaseModel)
- Services depend on interfaces, not implementations

### 3. Single Responsibility
- Each class has one reason to change
- Services focus on orchestration
- Models focus on AI operations
- Utils focus on specific operations

### 4. Open/Closed Principle
- Open for extension (new models via BaseModel)
- Closed for modification (existing code stable)
- New features added without changing core

### 5. DRY (Don't Repeat Yourself)
- Common operations in utilities
- Configuration centralized
- Validation logic reused

## Extensibility

### Adding New Models

```python
from src.models.base import BaseModel

class NewModel(BaseModel):
    def setup(self):
        # Initialize model
        pass
    
    def process(self, face_image, hairstyle_image, **kwargs):
        # Implement transfer
        pass
    
    def get_model_info(self):
        # Return metadata
        pass
```

### Adding New Services

```python
from src.config import get_settings
import logging

class NewService:
    def __init__(self):
        self.settings = get_settings()
        self.logger = logging.getLogger(__name__)
    
    def process(self, data):
        # Implement business logic
        pass
```

### Adding New Validators

```python
from src.utils.validators import ImageValidator

class CustomValidator(ImageValidator):
    def validate_custom(self, image):
        # Custom validation logic
        pass
```

## Security Considerations

### Input Validation
- All inputs validated before processing
- File size limits enforced
- File type restrictions
- Content validation

### Resource Management
- Process timeouts prevent hanging
- Temporary files cleaned up
- Memory limits considered
- Concurrent request handling

### Error Handling
- Comprehensive exception handling
- User-friendly error messages
- Detailed logging for debugging
- No sensitive data in logs

## Performance Optimization

### Lazy Initialization
- Models initialized on first use
- Resources loaded on demand
- Configuration cached

### Resource Cleanup
- Temporary files removed
- Model resources released
- Memory freed after processing

### Caching Strategies
- Settings singleton cached
- Gallery metadata cached
- Aligned images reused

## Testing Strategy

### Unit Tests
- Individual component testing
- Mock external dependencies
- Test edge cases

### Integration Tests
- Service layer testing
- End-to-end workflows
- Component interaction

### Test Coverage
- Configuration: 100%
- Validators: 95%+
- Services: 90%+
- Models: Integration level

## Monitoring and Logging

### Logging Levels
- INFO: Normal operations
- WARNING: Recoverable issues
- ERROR: Failed operations
- DEBUG: Detailed debugging

### Log Locations
- Console: Real-time feedback
- File: Persistent logs
- Structured: Easy parsing

### Metrics
- Processing time
- Success/failure rates
- Resource usage
- Error frequencies

## Deployment Architecture

### Local Development
```
Developer Machine
├── Python 3.10+ environment
├── Git repository
├── Local testing
└── Gradio dev server
```

### Production (Hugging Face Spaces)
```
HF Spaces Container
├── Python 3.10 runtime
├── Gradio server
├── Model weights (downloaded on startup)
├── Persistent storage (optional)
└── Public HTTPS endpoint
```

## Future Enhancements

### Planned Additions
1. Multiple model support
2. Batch processing
3. User history tracking
4. Advanced preprocessing
5. API rate limiting
6. Caching layer
7. Async processing
8. WebSocket support

### Scalability Considerations
- Horizontal scaling with load balancer
- Distributed model serving
- Cloud storage integration
- Database for user data
- Queue-based processing
