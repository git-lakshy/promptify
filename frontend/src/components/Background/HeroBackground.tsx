import { useEffect } from 'react';
import NoiseCanvas from './NoiseCanvas';

const HeroBackground = () => {
    useEffect(() => {
        const handleMouseMove = (e: MouseEvent) => {
            const moveX = (e.clientX - window.innerWidth / 2) * 0.01;
            const moveY = (e.clientY - window.innerHeight / 2) * 0.01;

            const glowBeam = document.querySelector('.glow-beam') as HTMLElement;
            if (glowBeam) {
                glowBeam.style.transform = `rotate(-15deg) translate(${moveX * -1}px, ${moveY * -1}px)`;
            }
        };

        document.addEventListener('mousemove', handleMouseMove);
        return () => document.removeEventListener('mousemove', handleMouseMove);
    }, []);

    return (
        <>
            <div className="hero-bg"></div>
            <div className="glow-beam"></div>
            <div className="ambient-fog"></div>
            <NoiseCanvas />
        </>
    );
};

export default HeroBackground;
