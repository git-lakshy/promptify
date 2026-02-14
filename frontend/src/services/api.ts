const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export interface EnhanceRequest {
    prompt: string;
    mode: 'normal' | 'advanced';
    fingerprint: string;
    user_api_key?: string;
}

export interface EnhanceResponse {
    enhanced_prompt?: string;
    provider_used?: string;
    mode: string;
    blocked: boolean;
    blocked_keywords: string[];
    rate_limited: boolean;
    rate_limit_message?: string;
    retry_after?: number;
    error?: string;
    usage?: any;
}

export const enhancePrompt = async (data: EnhanceRequest): Promise<EnhanceResponse> => {
    const response = await fetch(`${API_URL}/enhance`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to enhance prompt');
    }

    return response.json();
};
