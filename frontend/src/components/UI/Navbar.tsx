import pIcon from '../../assets/p-icon.png';

const Navbar = () => {
    return (
        <nav className="fixed top-0 w-full z-50 px-6 md:px-12 py-6">
            <div className="max-w-7xl mx-auto relative flex items-center justify-between">
                {/* Logo */}
                <div className="flex items-center gap-2 cursor-pointer group">
                    <div className="w-10 h-10 flex items-center justify-center overflow-visible">
                        <img src={pIcon} alt="Promptify" className="w-full h-full object-contain brightness-110" />
                    </div>
                    <span className="text-xl font-bold tracking-wide text-white drop-shadow-sm uppercase">
                        PROMPTIFY
                    </span>
                </div>

                {/* Center Nav Links */}
                <div className="hidden md:flex items-center gap-10 text-xs font-medium tracking-widest text-slate-300/90 uppercase absolute left-1/2 -translate-x-1/2">
                    <a href="#" className="hover:text-white transition-colors">Limits</a>
                    <a href="https://lakshyeah.in/my-work" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors flex items-center gap-1">
                        more
                        <i className="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                    </a>
                </div>

                {/* Language */}
                <div className="flex items-center gap-4">
                    <span className="text-xs text-slate-400 cursor-pointer hover:text-white">
                        EN
                    </span>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
