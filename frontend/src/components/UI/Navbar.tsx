import { Link } from 'react-router-dom';
import pIcon from '../../assets/p-icon.png';
import { useAuth } from '../../contexts/AuthContext';

const Navbar = () => {
    const { user, logout, isLoading } = useAuth();

    const handleLogout = () => {
        logout();
        window.location.reload();
    };

    return (
        <>
            {/* Desktop Navbar (Horizontal) */}
            <nav className="hidden md:block fixed top-0 w-full z-50 px-12 py-6">
                <div className="max-w-7xl mx-auto relative flex items-center justify-between">
                    <Link to="/" className="flex items-center gap-2 cursor-pointer group no-underline">
                        <div className="w-10 h-10 flex items-center justify-center overflow-visible hover:scale-110 active:scale-90 transition-transform duration-150 ease-out">
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
                        {isLoading ? (
                            <div className="w-16 h-4 bg-white/10 rounded animate-pulse" />
                        ) : user ? (
                            <div className="flex items-center gap-3">
                                <span className="text-xs text-slate-300 hidden lg:block">
                                    {user.name || user.email}
                                </span>
                                <button
                                    onClick={handleLogout}
                                    className="text-xs text-slate-400 hover:text-white transition-colors cursor-pointer px-3 py-1 rounded border border-white/10 hover:border-white/30"
                                >
                                    Logout
                                </button>
                            </div>
                        ) : (
                            <Link
                                to="/login"
                                className="text-xs text-white hover:text-blue-200 transition-colors px-4 py-2 rounded border border-white/20 hover:border-blue-400/50 hover:bg-blue-500/10"
                            >
                                Sign In
                            </Link>
                        )}
                    </div>
                </div>
            </nav>

            {/* Mobile Navbar (Vertical Sidebar on Left) */}
            <nav className="md:hidden fixed left-0 top-0 h-full w-[70px] z-50 flex flex-col items-center py-8 border-r border-white/10 bg-black/40 backdrop-blur-xl">
                <Link to="/" className="w-10 h-10 flex items-center justify-center mb-8 group">
                    <img src={pIcon} alt="Promptify" className="w-full h-full object-contain brightness-110 hover:scale-110 active:scale-90 transition-transform duration-150 ease-out" />
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

                <div className="mt-auto flex flex-col items-center space-y-4">
                    {isLoading ? (
                        <div className="w-6 h-6 rounded-full border-2 border-white/20 border-t-blue-400 animate-spin" />
                    ) : user ? (
                        <button
                            onClick={handleLogout}
                            className="text-[10px] text-slate-400 hover:text-white transition-colors whitespace-nowrap tracking-widest uppercase py-2"
                        >
                            Logout
                        </button>
                    ) : (
                        <Link
                            to="/login"
                            className="text-[10px] text-blue-300 hover:text-white transition-colors whitespace-nowrap tracking-widest uppercase py-2"
                        >
                            Sign In
                        </Link>
                    )}
                </div>
            </nav>
        </>
    );
};

export default Navbar;
