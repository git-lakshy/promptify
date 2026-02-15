import React, { useState } from 'react';

interface PromptInputProps {
    onSend: (prompt: string, mode: 'normal' | 'advanced', userApiKey: string) => void;
    isLoading: boolean;
}

const PromptInput: React.FC<PromptInputProps> = ({ onSend, isLoading }) => {
    const [prompt, setPrompt] = useState('');
    const [mode, setMode] = useState<'normal' | 'advanced'>('normal');
    const [userApiKey, setUserApiKey] = useState('');
    const [showKeyInput, setShowKeyInput] = useState(false);

    const handleSubmit = () => {
        if (prompt.trim() && !isLoading) {
            onSend(prompt, mode, userApiKey);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    return (
        <div className="w-full max-w-2xl mt-4 relative group flex flex-col items-center">
            <div className="glass-input-container dark-glass-input-container rounded-3xl p-2 flex flex-col transition-all duration-300 w-full">

                {/* Input Field */}
                <div className="flex items-center px-4 py-3">
                    <input
                        type="text"
                        placeholder="select mode and enter prompt to enhance..."
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                        onKeyDown={handleKeyDown}
                        disabled={isLoading}
                        className="flex-1 bg-transparent border-none text-slate-200 placeholder-slate-400 text-lg focus:outline-none font-light disabled:opacity-50"
                    />
                </div>

                {/* Bottom Tools Row */}
                <div className="flex items-center justify-between px-2 pb-2 mt-1">
                    <div className="flex items-center gap-2">
                        {/* normal mode*/}
                        <div className="relative group/tooltip">
                            <button
                                onClick={() => setMode('normal')}
                                className={`input-pill text-sm ${mode === 'normal' ? 'active' : ''}`}
                            >
                                <span>Normal</span>
                            </button>
                            {/* Tooltip */}
                            <div className="absolute top-full left-1/2 -translate-x-1/2 mt-2 px-3 py-1.5 bg-slate-900/90 backdrop-blur-md border border-white/10 rounded-lg text-[10px] text-white/90 whitespace-nowrap opacity-0 group-hover/tooltip:opacity-100 transition-opacity duration-200 pointer-events-none z-50 shadow-xl uppercase tracking-widest">
                                simple improvement
                            </div>
                        </div>

                        {/* advanced mode --> */}
                        <div className="relative group/tooltip">
                            <button
                                onClick={() => setMode('advanced')}
                                className={`input-pill text-sm ${mode === 'advanced' ? 'active' : ''}`}
                            >
                                <span>Advanced</span>
                            </button>
                            {/* Tooltip */}
                            <div className="absolute top-full left-1/2 -translate-x-1/2 mt-2 px-3 py-1.5 bg-slate-900/90 backdrop-blur-md border border-white/10 rounded-lg text-[10px] text-white/90 whitespace-nowrap opacity-0 group-hover/tooltip:opacity-100 transition-opacity duration-200 pointer-events-none z-50 shadow-xl uppercase tracking-widest">
                                detailed enhancement
                            </div>
                        </div>

                        {/* Skills.md Section (Paid) */}
                        <div className="relative group/tooltip">
                            <div className="input-pill text-sm opacity-40 cursor-help border-dashed border-white/20">
                                <span>Skills.md</span>
                            </div>
                            {/* Tooltip */}
                            <div className="absolute top-full left-1/2 -translate-x-1/2 mt-2 px-3 py-1.5 bg-slate-900/90 backdrop-blur-md border border-white/10 rounded-lg text-[10px] text-white/90 whitespace-nowrap opacity-0 group-hover/tooltip:opacity-100 transition-opacity duration-200 pointer-events-none z-50 shadow-xl uppercase tracking-widest">
                                paid feature : Create skills for your AI
                            </div>
                        </div>

                    </div>

                    {/* Send Button */}
                    <button
                        onClick={handleSubmit}
                        disabled={isLoading || !prompt.trim()}
                        className="send-btn w-10 h-10 rounded-full flex items-center justify-center text-white disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {isLoading ? (
                            <i className="fa-solid fa-spinner fa-spin text-sm"></i>
                        ) : (
                            <i className="fa-solid fa-arrow-right text-sm"></i>
                        )}
                    </button>
                </div>
            </div>

            {/* API Key Bypass */}
            <div className="mt-4 flex flex-col items-start gap-3 self-start pl-4">
                {!showKeyInput ? (
                    <button
                        onClick={() => setShowKeyInput(true)}
                        className="text-xs text-white/40 hover:text-white/80 transition-colors cursor-pointer"
                    >
                        Have a key?
                    </button>
                ) : (
                    <div className="flex flex-col items-start gap-2 animate-in fade-in slide-in-from-top-2 duration-300">
                        <div className="flex items-center gap-2 border-b border-dashed border-white/20 pb-1 px-1 relative min-w-[105px]">
                            <i className="fa-solid fa-key text-[10px] text-white/30"></i>

                            {/* Auto-growing input container */}
                            <div className="inline-grid items-center min-w-[90px]">
                                <span className="invisible row-start-1 col-start-1 text-xs whitespace-pre px-[1px] tracking-wider">
                                    {userApiKey || "Bypass limits with your own key"}
                                </span>
                                <input
                                    type="password"
                                    placeholder="Bypass limits with your own key"
                                    value={userApiKey}
                                    onChange={(e) => setUserApiKey(e.target.value)}
                                    className="row-start-1 col-start-1 bg-transparent border-none text-white/90 placeholder-white/20 text-[11px] focus:outline-none w-full font-light tracking-wider"
                                />
                            </div>

                            {userApiKey && (
                                <button onClick={() => setUserApiKey('')} className="text-white/40 hover:text-white/60 absolute -right-4">
                                    <i className="fa-solid fa-xmark text-[10px]"></i>
                                </button>
                            )}
                        </div>
                        <button
                            onClick={() => setShowKeyInput(false)}
                            className="text-[9px] text-white/40 hover:text-white/70 transition-colors uppercase tracking-[0.2em] mt-1"
                        >
                            Hide
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default PromptInput;
