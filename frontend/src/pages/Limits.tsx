import React from 'react';

const Limits: React.FC = () => {
    return (
        <main className="flex-grow flex flex-col items-center justify-center px-4 md:px-8 pt-24 pb-12 relative z-10">
            <div className="max-w-6xl w-full flex flex-col md:flex-row items-stretch justify-center gap-8 mt-10 min-h-[400px]">

                {/* Left Container */}
                <div className="flex-1 bg-white/[0.03] backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl relative overflow-hidden">
                    <div className="h-full w-full flex flex-col items-start space-y-8">
                        <div className="space-y-4 w-full group/line cursor-pointer">
                            <div className="w-12 h-1 bg-blue-400/30 rounded-full transition-all duration-300 group-hover/line:bg-blue-400/60 group-hover/line:shadow-[0_0_15px_rgba(96,165,250,0.5)]"></div>
                            <h2 className="text-sm font-medium text-white/90 uppercase tracking-[0.2em]">Free Tier</h2>
                        </div>

                        <table className="w-full text-left border-collapse">
                            <tbody className="text-slate-400 font-light text-sm space-y-4">
                                <tr className="border-b border-white/5">
                                    <td className="py-4 pr-4 uppercase tracking-tighter text-slate-500 text-[10px] font-medium">Mode</td>
                                    <td className="py-4 uppercase tracking-tighter text-slate-500 text-[10px] font-medium">Quota</td>
                                </tr>
                                <tr>
                                    <td className="py-4 text-slate-200">Normal</td>
                                    <td className="py-4">10 Hourly / 20 Daily</td>
                                </tr>
                                <tr>
                                    <td className="py-4 text-slate-200">Advanced</td>
                                    <td className="py-4">5 Hourly / 10 Daily</td>
                                </tr>
                                <tr>
                                    <td className="py-4 text-slate-200">Skills.md</td>
                                    <td className="py-4 text-red-500/80 font-medium uppercase tracking-tighter text-[15px]">No Access</td>
                                </tr>
                            </tbody>
                        </table>
                        <p className="text-[10px] text-slate-500 uppercase tracking-widest pt-4">
                            * You can use your own key to bypass free tier limits.
                        </p>
                    </div>
                </div>

                {/* Right Container */}
                <div className="flex-1 bg-white/[0.03] backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl relative overflow-hidden">
                    <div className="h-full w-full flex flex-col items-start space-y-8">
                        <div className="space-y-4 w-full group/line cursor-pointer">
                            <div className="w-12 h-1 bg-indigo-400/30 rounded-full transition-all duration-300 group-hover/line:bg-indigo-400/60 group-hover/line:shadow-[0_0_15px_rgba(129,140,248,0.5)]"></div>
                            <h2 className="text-sm font-medium text-white/90 uppercase tracking-[0.2em]">Paid Tier</h2>
                        </div>

                        <table className="w-full text-left border-collapse">
                            <tbody className="text-slate-400 font-light text-sm space-y-4">
                                <tr className="border-b border-white/5">
                                    <td className="py-4 pr-4 uppercase tracking-tighter text-slate-500 text-[10px] font-medium">Mode</td>
                                    <td className="py-4 uppercase tracking-tighter text-slate-500 text-[10px] font-medium">Quota</td>
                                </tr>
                                <tr>
                                    <td className="py-4 text-slate-300 font-light text-sm">Normal</td>
                                    <td className="py-4">
                                        <span className="text-indigo-400/90 font-medium uppercase tracking-tighter text-[15px] border-b border-dotted border-indigo-400/40 pb-0.5">Unlimited</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td className="py-4 text-slate-300 font-light text-sm">Advanced</td>
                                    <td className="py-4">
                                        <span className="text-indigo-400/90 font-medium uppercase tracking-tighter text-[15px] border-b border-dotted border-indigo-400/40 pb-0.5">Unlimited</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td className="py-4 text-indigo-400 font-bold drop-shadow-[0_0_8px_rgba(129,140,248,0.4)] text-sm">Skills.md</td>
                                    <td className="py-4">
                                        <span className="text-indigo-400 font-bold uppercase tracking-tighter text-[15px] drop-shadow-[0_0_8px_rgba(129,140,248,0.4)] border-b border-dotted border-indigo-400/60 pb-0.5">Unlimited</span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <p className="text-[10px] text-slate-500 uppercase tracking-widest pt-4">
                            One time purchase to bypass all limits.
                        </p>
                    </div>
                </div>

            </div>
        </main>
    );
};

export default Limits;
