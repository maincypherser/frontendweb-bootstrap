from rest_framework import serializers
from .models import User, Organization, OrgUser, Agent, Log, Policy


# ===========================
# User Serializer
# ===========================

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    password = serializers.CharField(write_only=True)  # Ensure password is write-only
    organization_id = serializers.UUIDField(write_only=True, required=False)  # Added organization_id field

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'role', 'is_active', 'organization_id']

    def create(self, validated_data):
        """Override create method to handle password and organization properly."""
        organization_id = validated_data.pop('organization_id', None)  # Extract organization ID
        password = validated_data.pop('password', None)  # Remove password from validated_data
        user = super().create(validated_data)  # Create the user without the password
        if password:
            user.set_password(password)  # Set the hashed password
            user.save()  # Save the user with the hashed password

        if organization_id:  # Link user to organization if provided
            try:
                org = Organization.objects.get(id=organization_id)
                # Check if OrgUser already exists for this user
                OrgUser.objects.get_or_create(user=user, organization=org, is_org_admin=(user.role == 'org_admin'))
            except Organization.DoesNotExist:
                raise serializers.ValidationError("Organization with this ID does not exist.")

        return user

    def update(self, instance, validated_data):
        """Override update method to handle password properly."""
        organization_id = validated_data.pop('organization_id', None)  # Extract organization ID if updating
        password = validated_data.pop('password', None)  # Remove password from validated_data
        user = super().update(instance, validated_data)  # Update the user without the password
        if password:
            user.set_password(password)  # Set the hashed password
            user.save()  # Save the user with the new hashed password

        if organization_id:  # Update organization link if provided
            try:
                org = Organization.objects.get(id=organization_id)
                OrgUser.objects.update_or_create(user=user, organization=org)  # Create or update OrgUser link
            except Organization.DoesNotExist:
                raise serializers.ValidationError("Organization with this ID does not exist.")

        return user

# ===========================
# Organization Serializer
# ===========================

class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for the Organization model."""

    class Meta:
        model = Organization
        fields = ['id', 'name', 'created_by', 'created_at']  # Removed org_id reference

# ===========================
# OrgUser Serializer
# ===========================

class OrgUserSerializer(serializers.ModelSerializer):
    """Serializer for the OrgUser model."""

    class Meta:
        model = OrgUser
        fields = ['id', 'user', 'organization', 'is_org_admin']

# ===========================
# Agent Serializer
# ===========================

class AgentSerializer(serializers.ModelSerializer):
    """Serializer for the Agent model, handling different agent types."""

    class Meta:
        model = Agent
        fields = ['id', 'user', 'organization', 'device_type', 'operating_system', 'browser_type', 'agent_version', 'last_checkin', 'active']
        read_only_fields = ['user', 'organization', 'id', 'last_checkin', 'active']  # Mark user and organization as read-only

# ===========================
# Log Serializer
# ===========================

class LogSerializer(serializers.ModelSerializer):
    """Serializer for the unified Log model."""

    class Meta:
        model = Log
        fields = ['id', 'agent', 'timestamp', 'alert_or_event', 'log_type', 'key_field', 'description',
                  'additional_data']
        read_only_fields = ['id', 'timestamp']  # Auto-generated fields

    def validate(self, data):
        """Custom validation based on log type and alert/event status."""
        log_type = data.get('log_type')
        alert_or_event = data.get('alert_or_event')
        key_field = data.get('key_field')

        # Validate required fields for events and alerts
        if not data.get('agent'):
            raise serializers.ValidationError("Agent is required.")

        # Event-specific validation
        if alert_or_event == 'event':
            if not log_type:
                raise serializers.ValidationError("Log type must be specified for events.")
            if not key_field:
                raise serializers.ValidationError(f"Key field must be provided for {log_type} logs.")

        # Alert-specific validation (you can add more rules here)
        if alert_or_event == 'alert':
            if not data.get('description'):
                raise serializers.ValidationError("Description must be provided for alerts.")

        return data



# ===========================
# Policy Serializer
# ===========================
class PolicySerializer(serializers.ModelSerializer):
    """Serializer for the Policy model."""

    class Meta:
        model = Policy
        fields = [
            'id', 'name', 'description', 'policy_type', 'organization', 'editable',
            'blocked_url_categories', 'custom_blocked_urls',
            'blocked_phone_categories', 'custom_blocked_phone_numbers',
            'static_web_analysis_categories', 'ai_web_analysis_enabled',
            'identity_monitoring_enabled', 'configuration_monitoring'
        ]
        read_only_fields = ['editable', 'policy_type']  # Make these fields read-only

    def create(self, validated_data):
        """Custom creation logic for policies."""
        # Only allow Org Admins to create custom policies (editable)
        user = self.context['request'].user
        if user.role == 'org_admin':
            validated_data['policy_type'] = 'custom'
            validated_data['editable'] = True
            validated_data['organization'] = user.orguser.organization  # Ensure it is tied to their org
        elif user.role in ['platform_admin', 'superuser']:
            # Platform admins and superusers can create default policies
            validated_data['policy_type'] = 'default'
            validated_data['editable'] = False
        else:
            raise serializers.ValidationError("You do not have permission to create a policy.")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Ensure only custom policies can be edited by Org Admins."""
        if not instance.editable:
            raise serializers.ValidationError("Default policies cannot be edited.")
        return super().update(instance, validated_data)