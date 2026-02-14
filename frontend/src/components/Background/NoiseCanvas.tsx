import { useEffect, useRef } from 'react';

const NoiseCanvas = () => {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let width: number, height: number;

        const resize = () => {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
            generateNoise();
        };

        const generateNoise = () => {
            const imageData = ctx.createImageData(width, height);
            const data = imageData.data;

            for (let i = 0; i < data.length; i += 4) {
                const value = Math.random() * 255;
                data[i] = value;     // red
                data[i + 1] = value; // green
                data[i + 2] = value; // blue
                data[i + 3] = 255;   // alpha
            }

            ctx.putImageData(imageData, 0, 0);
        };

        window.addEventListener('resize', resize);
        resize();

        return () => window.removeEventListener('resize', resize);
    }, []);

    return <canvas id="noise-canvas" ref={canvasRef} />;
};

export default NoiseCanvas;
