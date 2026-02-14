interface FooterProps {
    onUpgradeClick: () => void;
}

const Footer: React.FC<FooterProps> = ({ onUpgradeClick }) => {
    return (
        <footer className="w-full px-6 md:px-12 py-8 relative z-10 mt-auto">
            <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-end gap-6">
                {/* Left: Scroll Indicator */}
                <div className="flex items-center gap-2 text-slate-500 hover:text-slate-300 transition-colors cursor-pointer">
                    <i className="fa-solid fa-arrow-down animate-bounce text-xs"></i>
                </div>

                {/* Center: Subtext */}
                <div className="text-left md:text-center text-xs text-slate-400/80 max-w-sm leading-relaxed">
                    Promptify uses AI to transform raw ideas into powerful prompts.
                    From a simple thought to a refined command — instantly.
                </div>

                {/* Right: Upgrade */}
                <button
                    onClick={onUpgradeClick}
                    className="px-5 py-2.5 rounded-lg border border-white/20 hover:border-white/40 hover:bg-white/5 text-slate-200 transition-all text-sm flex items-center gap-2 group cursor-pointer"
                >
                    Upgrade
                    <i className="fa-solid fa-arrow-right text-xs group-hover:translate-x-1 transition-transform"></i>
                </button>
            </div>
        </footer>
    );
};

export default Footer;
