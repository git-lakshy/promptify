import { Link } from 'react-router-dom';
import pIcon from '../../assets/p-icon.png';

const Navbar = () => {

    return (
        <>
            {/* Desktop Navbar (Horizontal) */}
            <nav className="hidden md:block fixed top-0 w-full z-50 px-12 py-6">
                <div className="max-w-7xl mx-auto relative flex items-center justify-between">
                    <Link to="/" className="flex items-center gap-2 cursor-pointer group no-underline">
                        <div className="w-10 h-10 flex items-center justify-center overflow-visible">
                            <img src={pIcon} alt="Promptify" className="w-full h-full object-contain brightness-110" />
                        </div>
                        <span className="text-xl font-bold tracking-wide text-white drop-shadow-sm uppercase">
                            PROMPTIFY
                        </span>
                    </Link>

                    <div className="flex items-center gap-10 text-xs font-medium tracking-widest text-slate-300/90 uppercase absolute left-1/2 -translate-x-1/2">
                        <Link to="/" className="hover:text-white transition-colors no-underline">Enhance</Link>
                        <Link to="/limits" className="hover:text-white transition-colors no-underline">Limits</Link>
                        <a href="https://lakshyeah.in/my-work" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors flex items-center gap-1 no-underline">
                            more
                            <i className="fa-solid fa-arrow-up-right-from-square text-[10px]"></i>
                        </a>
                    </div>

                    <div className="flex items-center gap-4">
                        <span className="text-xs text-slate-400 cursor-pointer hover:text-white">
                            EN
                        </span>
                    </div>
                </div>
            </nav>

            {/* Mobile Navbar (Vertical Sidebar on Left) */}
            <nav className="md:hidden fixed left-0 top-0 h-full w-[70px] z-50 flex flex-col items-center py-8 border-r border-white/10 bg-black/40 backdrop-blur-xl">
                <Link to="/" className="w-10 h-10 flex items-center justify-center mb-12">
                    <img src={pIcon} alt="Promptify" className="w-full h-full object-contain brightness-110" />
                </Link>

                <div className="flex-grow flex flex-col items-center space-y-8">
                    <Link to="/" className="text-white/60 hover:text-white transition-colors whitespace-nowrap text-[10px] font-medium tracking-[0.2em] uppercase py-2">
                        Enhance
                    </Link>
                    <Link to="/limits" className="text-white/60 hover:text-white transition-colors whitespace-nowrap text-[10px] font-medium tracking-[0.2em] uppercase py-2">
                        Limits
                    </Link>
                    <a href="https://lakshyeah.in/my-work" target="_blank" rel="noopener noreferrer" className="text-white/60 hover:text-white transition-colors whitespace-nowrap text-[10px] font-medium tracking-[0.2em] uppercase py-2">
                        more
                    </a>
                </div>

                <div className="mt-auto">
                    <span className="text-[10px] text-slate-500 font-bold uppercase tracking-widest cursor-pointer hover:text-white">
                        EN
                    </span>
                </div>
            </nav>
        </>
    );
};

export default Navbar;
