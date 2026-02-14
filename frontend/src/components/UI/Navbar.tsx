import { Link } from 'react-router-dom';
import pIcon from '../../assets/p-icon.png';

const Navbar = () => {
    return (
        <nav className="fixed top-0 w-full z-50 px-6 md:px-12 py-6">
            <div className="max-w-7xl mx-auto relative flex items-center justify-between">
                {/* Logo */}
                <Link to="/" className="flex items-center gap-2 cursor-pointer group no-underline">
                    <div className="w-10 h-10 flex items-center justify-center overflow-visible">
                        <img src={pIcon} alt="Promptify" className="w-full h-full object-contain brightness-110" />
                    </div>
                    <span className="text-xl font-bold tracking-wide text-white drop-shadow-sm uppercase">
                        PROMPTIFY
                    </span>
                </Link>

                {/* Center Nav Links */}
                <div className="hidden md:flex items-center gap-10 text-xs font-medium tracking-widest text-slate-300/90 uppercase absolute left-1/2 -translate-x-1/2">
                    <Link to="/" className="hover:text-white transition-colors no-underline">Enhance</Link>
                    <Link to="/limits" className="hover:text-white transition-colors no-underline">Limits</Link>
                    <a href="https://lakshyeah.in/my-work" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors flex items-center gap-1 no-underline">
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
