import os, joblib, json
import pandas as pd
import numpy as np

from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PredictionHistory
from .serializers import RegisterSerializer, UserSerializer, PredictionHistorySerializer


# ------------------------ LOAD MODELS ------------------------
PIPELINE_PATH = os.path.join(settings.BASE_DIR, "artifacts", "pipeline.pkl")
LE_PATH = os.path.join(settings.BASE_DIR, "artifacts", "label_encoder.pkl")

PIPELINE = None
LE = None

try:
    PIPELINE = joblib.load(PIPELINE_PATH)
    print("ML Pipeline Loaded Successfully!")
except Exception as e:
    print("❌ Pipeline Load Error:", e)

try:
    LE = joblib.load(LE_PATH)
    print("Label Encoder Loaded Successfully!")
except Exception as e:
    print("❌ Label Encoder Load Error:", e)



# ------------------------ REGISTER ------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=201)
    return Response(serializer.errors, status=400)



# ------------------------ LOGIN ------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username
        })
    
    return Response({"error": "Invalid username or password"}, status=401)



# ------------------------ PROFILE ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    return Response(UserSerializer(request.user).data)



# ------------------------ PREDICT ------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_view(request):

    # check model loaded
    if PIPELINE is None or LE is None:
        return Response({"error": "Model not loaded on server"}, status=500)

    data = request.data

    # REQUIRED fields
    required_fields = [
        "CGPA", "Years of Experience", "Degree", "Major", 
        "Specialization", "Certification", "Preferred Industry", "Skills"
    ]

    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        return Response({
            "error": "Please fill all fields",
            "missing_fields": missing
        }, status=400)

    # Construct row for prediction
    row = {
        "CGPA": float(data.get("CGPA")),
        "Years of Experience": float(data.get("Years of Experience")),
        "Degree": data.get("Degree").strip(),
        "Major": data.get("Major").strip(),
        "Specialization": data.get("Specialization").strip(),
        "Certification": data.get("Certification").strip(),
        "Preferred Industry": data.get("Preferred Industry").strip(),
        "Skills": data.get("Skills") or data.get("skills") or ""
    }

    df = pd.DataFrame([row])

    try:
        # Prediction
        pred_enc = PIPELINE.predict(df)
        pred_label = LE.inverse_transform(pred_enc)[0]

        # Probability for all classes
        prob = PIPELINE.predict_proba(df)[0]

        # Top 3 roles
        top3_idx = np.argsort(prob)[::-1][:3]
        top3_roles = LE.inverse_transform(top3_idx).tolist()
        top3_prob = (prob[top3_idx] * 100).round(2).tolist()

        # Save history
        PredictionHistory.objects.create(
            user=request.user,
            input_data=json.dumps(row),
            predicted=pred_label
        )

        # FINAL result for result.html
        return Response({
            "predicted_role": pred_label,
            "top3_roles": top3_roles,
            "top3_probabilities": top3_prob
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)



# ------------------------ HISTORY ------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history_view(request):
    qs = PredictionHistory.objects.filter(user=request.user).order_by("-created_at")
    ser = PredictionHistorySerializer(qs, many=True)
    return Response(ser.data)



# ------------------------ LOGOUT ------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_view(request):
    if PIPELINE is None or LE is None:
        return Response({'error': 'ML model not available on server.'}, status=500)

    required_fields = [
        'CGPA',
        'Years of Experience',
        'Degree',
        'Major',
        'Specialization',
        'Certification',
        'Preferred Industry',
        'Skills'
    ]

    # ❌ Check missing fields
    missing = [f for f in required_fields if f not in request.data or request.data.get(f) in ["", None]]
    if missing:
        return Response({
            'error': 'Please fill all fields.',
            'missing_fields': missing
        }, status=400)

    # Build row
    numeric_cols = ['CGPA', 'Years of Experience']
    categorical_cols = ['Degree','Major','Specialization','Certification','Preferred Industry']

    row = {}
    for c in numeric_cols:
        row[c] = float(request.data[c])

    for c in categorical_cols:
        row[c] = request.data[c].strip()

    row['Skills'] = request.data['Skills'].strip()

    df = pd.DataFrame([row])

    try:
        # 🔥 Predict probabilities
        probs = PIPELINE.predict_proba(df)[0]

        # 🔥 Get top 3 jobs
        top3_idx = probs.argsort()[-3:][::-1]
        top3_roles = [LE.inverse_transform([i])[0] for i in top3_idx]
        top3_probs = [float(probs[i] * 100) for i in top3_idx]

        # Save history (store only best role)
        PredictionHistory.objects.create(
            user=request.user,
            input_data=json.dumps(row),
            predicted=top3_roles[0]
        )

        return Response({
            'top3_roles': top3_roles,
            'top3_probabilities': top3_probs
        })

    except Exception as e:
        return Response({'error': str(e)}, status=500)