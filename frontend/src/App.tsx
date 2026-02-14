import { useState, useEffect } from 'react';
import Navbar from './components/UI/Navbar';
import Footer from './components/UI/Footer';
import HeroBackground from './components/Background/HeroBackground';
import PromptInput from './components/UI/PromptInput';
import OutputDisplay from './components/UI/OutputDisplay';
import Notification from './components/UI/Notification';
import { enhancePrompt } from './services/api';
import type { EnhanceResponse } from './services/api';

import { Routes, Route } from 'react-router-dom';
import Limits from './pages/Limits';
import { Analytics } from '@vercel/analytics/next';

function Home({ onSend, isLoading, response }: any) {
    return (
        <main className="flex-grow flex flex-col items-center justify-center px-4 md:px-8 pt-24 pb-12 relative z-10">
            <div className="max-w-4xl w-full flex flex-col items-center text-center space-y-10 mt-10">
                <div className="space-y-2">
                    <h1 className="hero-title text-4xl md:text-6xl lg:text-7xl text-white leading-[1.1]">
                        Promptify - prompt <span className="dotted-underline text-blue-200">better</span> Turn <span className="dotted-underline text-white/90">ideas</span> into <span className="dotted-underline text-white/90">instructions</span>.
                    </h1>
                </div>
                <PromptInput onSend={onSend} isLoading={isLoading} />
                <OutputDisplay
                    content={response?.enhanced_prompt || ''}
                    isVisible={!!response?.enhanced_prompt}
                    error={response?.error || response?.rate_limit_message}
                    blocked={response?.blocked}
                />
            </div>
        </main>
    );
}

function App() {
    const [isLoading, setIsLoading] = useState(false);
    const [response, setResponse] = useState<EnhanceResponse | null>(null);
    const [fingerprint, setFingerprint] = useState('');
    const [showNotification, setShowNotification] = useState(false);

    useEffect(() => {
        let fp = localStorage.getItem('promptify_fp');
        if (!fp) {
            fp = crypto.randomUUID();
            localStorage.setItem('promptify_fp', fp);
        }
        setFingerprint(fp);
    }, []);

    const handleSend = async (prompt: string, mode: 'normal' | 'advanced', userApiKey: string) => {
        setIsLoading(true);
        setResponse(null);
        try {
            const result = await enhancePrompt({
                prompt,
                mode,
                fingerprint,
                user_api_key: userApiKey,
            });
            setResponse(result);
        } catch (error: any) {
            setResponse({
                mode,
                blocked: false,
                blocked_keywords: [],
                rate_limited: false,
                error: error.message || 'An unexpected error occurred.',
            } as EnhanceResponse);
        } finally {
            setIsLoading(false);
        }
    };

    const handleUpgrade = () => {
        setShowNotification(true);
        setTimeout(() => {
            setShowNotification(false);
        }, 5000);
    };

    return (
        <div className="min-h-screen flex flex-col relative overflow-hidden">
            <Analytics />
            <HeroBackground />
            <Navbar />

            <Notification
                message="Upgrading will soon be available for now you can use your own key to Bypass limits."
                isVisible={showNotification}
                onClose={() => setShowNotification(false)}
            />

            <Routes>
                <Route path="/" element={
                    <Home onSend={handleSend} isLoading={isLoading} response={response} />
                } />
                <Route path="/limits" element={<Limits />} />
            </Routes>

            <Footer onUpgradeClick={handleUpgrade} />
        </div>
    );
}

export default App;
