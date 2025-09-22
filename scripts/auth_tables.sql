-- ====================================================================
-- AUTHENTICATION TABLES FOR ONEQLICK FOOD DELIVERY APP
-- ====================================================================

-- Refresh tokens table for JWT refresh mechanism
CREATE TABLE core_mstr_one_qlick_refresh_tokens_tbl (
    refresh_token_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    is_revoked BOOLEAN DEFAULT FALSE,
    device_info JSONB, -- Store device fingerprint for security
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- OAuth providers table for social login
CREATE TABLE core_mstr_one_qlick_oauth_providers_tbl (
    oauth_provider_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL, -- 'google', 'facebook', 'apple'
    provider_user_id VARCHAR(255) NOT NULL,
    provider_email VARCHAR(255),
    provider_name VARCHAR(255),
    provider_photo_url VARCHAR(500),
    access_token_hash VARCHAR(255), -- Encrypted access token
    refresh_token_hash VARCHAR(255), -- Encrypted refresh token
    token_expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(provider, provider_user_id)
);

-- OTP verification table for phone/email verification
CREATE TABLE core_mstr_one_qlick_otp_verifications_tbl (
    otp_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    phone VARCHAR(20),
    email VARCHAR(255),
    otp_code VARCHAR(10) NOT NULL,
    otp_type VARCHAR(20) NOT NULL, -- 'phone_verification', 'email_verification', 'password_reset'
    expires_at TIMESTAMP NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    attempts INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User sessions table for tracking active sessions
CREATE TABLE core_mstr_one_qlick_user_sessions_tbl (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    device_id VARCHAR(255) NOT NULL,
    device_name VARCHAR(255),
    device_type VARCHAR(50), -- 'mobile', 'web', 'tablet'
    platform VARCHAR(50), -- 'ios', 'android', 'web'
    app_version VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, device_id)
);

-- Password reset tokens table
CREATE TABLE core_mstr_one_qlick_password_reset_tokens_tbl (
    reset_token_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ====================================================================
-- INDEXES FOR AUTHENTICATION TABLES
-- ====================================================================

-- Refresh tokens indexes
CREATE INDEX idx_one_qlick_refresh_tokens_user_id ON core_mstr_one_qlick_refresh_tokens_tbl(user_id);
CREATE INDEX idx_one_qlick_refresh_tokens_token_hash ON core_mstr_one_qlick_refresh_tokens_tbl(token_hash);
CREATE INDEX idx_one_qlick_refresh_tokens_expires_at ON core_mstr_one_qlick_refresh_tokens_tbl(expires_at);

-- OAuth providers indexes
CREATE INDEX idx_one_qlick_oauth_providers_user_id ON core_mstr_one_qlick_oauth_providers_tbl(user_id);
CREATE INDEX idx_one_qlick_oauth_providers_provider ON core_mstr_one_qlick_oauth_providers_tbl(provider);
CREATE INDEX idx_one_qlick_oauth_providers_provider_user_id ON core_mstr_one_qlick_oauth_providers_tbl(provider, provider_user_id);

-- OTP verification indexes
CREATE INDEX idx_one_qlick_otp_verifications_user_id ON core_mstr_one_qlick_otp_verifications_tbl(user_id);
CREATE INDEX idx_one_qlick_otp_verifications_phone ON core_mstr_one_qlick_otp_verifications_tbl(phone);
CREATE INDEX idx_one_qlick_otp_verifications_email ON core_mstr_one_qlick_otp_verifications_tbl(email);
CREATE INDEX idx_one_qlick_otp_verifications_expires_at ON core_mstr_one_qlick_otp_verifications_tbl(expires_at);

-- User sessions indexes
CREATE INDEX idx_one_qlick_user_sessions_user_id ON core_mstr_one_qlick_user_sessions_tbl(user_id);
CREATE INDEX idx_one_qlick_user_sessions_device_id ON core_mstr_one_qlick_user_sessions_tbl(device_id);
CREATE INDEX idx_one_qlick_user_sessions_active ON core_mstr_one_qlick_user_sessions_tbl(is_active);

-- Password reset tokens indexes
CREATE INDEX idx_one_qlick_password_reset_tokens_user_id ON core_mstr_one_qlick_password_reset_tokens_tbl(user_id);
CREATE INDEX idx_one_qlick_password_reset_tokens_token_hash ON core_mstr_one_qlick_password_reset_tokens_tbl(token_hash);
CREATE INDEX idx_one_qlick_password_reset_tokens_expires_at ON core_mstr_one_qlick_password_reset_tokens_tbl(expires_at);

-- ====================================================================
-- TRIGGERS FOR AUTHENTICATION TABLES
-- ====================================================================

-- Add triggers for updated_at timestamps
CREATE TRIGGER update_one_qlick_refresh_tokens_updated_at
    BEFORE UPDATE ON core_mstr_one_qlick_refresh_tokens_tbl
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_one_qlick_oauth_providers_updated_at
    BEFORE UPDATE ON core_mstr_one_qlick_oauth_providers_tbl
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_one_qlick_user_sessions_updated_at
    BEFORE UPDATE ON core_mstr_one_qlick_user_sessions_tbl
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ====================================================================
-- CLEANUP FUNCTIONS FOR EXPIRED TOKENS
-- ====================================================================

-- Function to clean up expired refresh tokens
CREATE OR REPLACE FUNCTION cleanup_expired_refresh_tokens()
RETURNS void AS $$
BEGIN
    DELETE FROM core_mstr_one_qlick_refresh_tokens_tbl 
    WHERE expires_at < CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;

-- Function to clean up expired OTP codes
CREATE OR REPLACE FUNCTION cleanup_expired_otp_codes()
RETURNS void AS $$
BEGIN
    DELETE FROM core_mstr_one_qlick_otp_verifications_tbl 
    WHERE expires_at < CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;

-- Function to clean up expired password reset tokens
CREATE OR REPLACE FUNCTION cleanup_expired_password_reset_tokens()
RETURNS void AS $$
BEGIN
    DELETE FROM core_mstr_one_qlick_password_reset_tokens_tbl 
    WHERE expires_at < CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;

-- ====================================================================
-- COMPLETION MESSAGE
-- ====================================================================

SELECT 'Authentication tables for OneQlick created successfully!' as status;
