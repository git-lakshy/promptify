import React from 'react';

interface NotificationProps {
    message: string;
    isVisible: boolean;
    onClose: () => void;
}

const Notification: React.FC<NotificationProps> = ({ message, isVisible, onClose }) => {
    return (
        <div
            className={`fixed top-6 right-6 z-[100] max-w-sm w-full transition-all duration-500 ease-out transform ${isVisible ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0 pointer-events-none'
                }`}
        >
            <div className="relative overflow-hidden rounded-xl bg-white/5 backdrop-blur-xl border border-white/20 shadow-2xl">
                <div className="p-4 flex items-start justify-between gap-3">
                    <p className="text-slate-200 text-sm leading-relaxed font-light tracking-wide">
                        {message}
                    </p>

                    <button
                        onClick={onClose}
                        className="text-white/30 hover:text-white transition-colors p-1 shrink-0"
                    >
                        <i className="fa-solid fa-xmark text-xs"></i>
                    </button>
                </div>

                {/* Bottom simple progress line highlight */}
                <div className="absolute bottom-0 left-0 h-[2px] bg-white/10 w-full animate-progress-shrink" />
            </div>
        </div>
    );
};

export default Notification;
