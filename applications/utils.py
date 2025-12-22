import os
from django.db import models

from django.db import models
from django.contrib.auth.models import User

import os



def candidate_photo_path(instance, filename):
    # Clean name for folder (avoid spaces & special chars)
    name = instance.name.replace(" ", "_") if instance.name else "unknown"
    return os.path.join("candidate_photos", name, filename)




