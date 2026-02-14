import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface OutputDisplayProps {
    content: string;
    isVisible: boolean;
    error?: string;
    blocked?: boolean;
}

const OutputDisplay: React.FC<OutputDisplayProps> = ({ content, isVisible, error, blocked }) => {
    const [copied, setCopied] = useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(content);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    if (!isVisible && !error && !blocked) return null;

    return (
        <AnimatePresence>
            {(isVisible || error || blocked) && (
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className="w-full max-w-2xl mt-6 relative"
                >
                    <div className="glass-input-container output-glass-container rounded-3xl p-6 transition-all duration-300">
                        <div className="flex justify-between items-start mb-4">
                            <h3 className="text-sm font-medium text-slate-400 uppercase tracking-widest">
                                {error ? 'Error' : blocked ? 'Blocked' : 'Enhanced Prompt'}
                            </h3>
                            {content && !error && !blocked && (
                                <button
                                    onClick={handleCopy}
                                    className="text-slate-400 hover:text-white transition-colors flex items-center gap-2 text-xs"
                                >
                                    {copied ? (
                                        <>
                                            <i className="fa-solid fa-check text-green-400"></i>
                                            <span>Copied</span>
                                        </>
                                    ) : (
                                        <>
                                            <i className="fa-solid fa-copy"></i>
                                            <span>Copy</span>
                                        </>
                                    )}
                                </button>
                            )}
                        </div>

                        <div className={`${error || blocked ? 'text-red-400' : 'text-slate-200'} text-lg font-light leading-relaxed whitespace-pre-wrap`}>
                            {error || content || (blocked && 'Content blocked by safety filters.')}
                        </div>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
};

export default OutputDisplay;
