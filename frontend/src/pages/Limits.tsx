import React from 'react';

const Limits: React.FC = () => {
    return (
        <main className="flex-grow flex flex-col items-center justify-center px-4 md:px-8 pt-24 pb-12 relative z-10">
            <div className="max-w-6xl w-full flex flex-col md:flex-row items-stretch justify-center gap-8 mt-10 min-h-[400px]">

                {/* Left Container */}
                <div className="flex-1 bg-white/[0.03] backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl relative overflow-hidden group hover:bg-white/[0.05] transition-all duration-500">
                    {/* Content placeholder */}
                    <div className="h-full w-full flex flex-col items-start space-y-4">
                        <div className="w-12 h-1 w-1/4 bg-blue-400/30 rounded-full"></div>
                        <h2 className="text-2xl font-semibold text-white/90 tracking-tight">Free Tier</h2>
                        <p className="text-slate-400 font-light leading-relaxed">
                            Limits analysis will appear here.
                        </p>
                    </div>
                </div>

                {/* Right Container */}
                <div className="flex-1 bg-white/[0.03] backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl relative overflow-hidden group hover:bg-white/[0.05] transition-all duration-500">
                    {/* Content placeholder */}
                    <div className="h-full w-full flex flex-col items-start space-y-4">
                        <div className="w-12 h-1 w-1/4 bg-indigo-400/30 rounded-full"></div>
                        <h2 className="text-2xl font-semibold text-white/90 tracking-tight">Paid Access</h2>
                        <p className="text-slate-400 font-light leading-relaxed">
                            Bypass details will appear here.
                        </p>
                    </div>
                </div>

            </div>
        </main>
    );
};

export default Limits;
