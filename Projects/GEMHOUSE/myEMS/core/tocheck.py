# # Use APIView for consistency:
#
#    # It's more secure since it supports DRF’s authentication (like JWT, session, token-based auth) and permission classes.
#     #Allows better separation of HTTP methods (GET, POST, PUT, etc.).
#
# #Ensure authentication and permission classes:
#
#    #  By default, APIView doesn’t enforce any authentication. You should explicitly add it:
#
# python
#
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
#
# class ScrapeAndStoreAPIView(APIView):
#     authentication_classes = [TokenAuthentication, BasicAuthentication]  # Use your preferred authentication
#     permission_classes = [IsAuthenticated]  # Only authenticated users can access this API
#
# # Add throttle for rate limiting:
#
#  #   You can use Django’s throttling features to prevent abuse (e.g., denial of service attacks):
#
# python
#
# from rest_framework.throttling import UserRateThrottle
#
# class ScrapeAndStoreAPIView(APIView):
#     throttle_classes = [UserRateThrottle]
#     # Adjust settings in settings.py for the rate limits
#
#
#
#
# Summary of Changes:
#
#     Access Token: Store the access token in memory (use useAuth context) to avoid storing it in localStorage.
#     Refresh Token: Store the refresh token in an HTTP-only cookie on the server side for security.
#     Token Expiry: Automatically refresh the access token using the refresh token when it expires.
#     Logout: Properly handle logout by clearing both the access token and the refresh token.