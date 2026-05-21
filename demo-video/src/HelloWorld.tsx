import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from 'remotion';

export const HelloWorld: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, fps / 2], [0, 1], { extrapolateRight: 'clamp' });
  const scale = interpolate(frame, [0, fps / 2], [0.8, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div
        style={{
          opacity,
          transform: `scale(${scale})`,
          color: 'white',
          fontSize: 80,
          fontWeight: 'bold',
          fontFamily: 'sans-serif',
          textAlign: 'center',
        }}
      >
        Hello World!
      </div>
    </AbsoluteFill>
  );
};
