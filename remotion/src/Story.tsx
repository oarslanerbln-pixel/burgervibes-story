// One 9:16 story frame. Same three presets as tools/story.py, but with
// real motion design: springs instead of linear slides, per-word timing and
// a neon tube that ignites letter by letter.
//   neon  - headline ignites like the restaurant's neon sign (flicker, then hold)
//   punch - words slam in from the left one after another
//   ask   - question pops in; a chevron points at the empty sticker zone
import React from 'react';
import {
  AbsoluteFill,
  Img,
  OffthreadVideo,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {C, SAFE_TOP, Tag, isVideo, neonGlow, useBrandFonts} from './brand';

export type StoryProps = {
  title: string;
  sub?: string;
  scriptSub?: boolean;
  preset: 'neon' | 'punch' | 'ask';
  accent: 'pink' | 'cyan';
  bg?: string; // path inside assets/, e.g. "ai/W1-Mo-1.png" or "selects/W1-Mo-2.mp4"
  duration?: number; // seconds
};

// Deterministic flicker: the same frame always renders the same way.
const flicker = (frame: number, start: number) => {
  const f = frame - start;
  if (f < 0) return 0;
  const pattern = [1, 0.2, 1, 1, 0, 0.9, 1, 0.3, 1];
  return f < pattern.length * 2 ? pattern[Math.floor(f / 2)] : 1;
};

const Background: React.FC<{bg?: string}> = ({bg}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const scale = interpolate(frame, [0, durationInFrames], [1, 1.08]);
  if (!bg) {
    return (
      <AbsoluteFill
        style={{
          background: `radial-gradient(60% 40% at 15% 75%, ${C.pink}99, transparent 70%),
                       radial-gradient(55% 35% at 85% 35%, ${C.cyan}77, transparent 70%), ${C.ink}`,
        }}
      />
    );
  }
  const src = staticFile(bg);
  return (
    <AbsoluteFill style={{transform: `scale(${scale})`}}>
      {isVideo(bg) ? (
        <OffthreadVideo src={src} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      ) : (
        <Img src={src} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      )}
    </AbsoluteFill>
  );
};

export const Story: React.FC<StoryProps> = ({title, sub, scriptSub, preset, accent, bg}) => {
  useBrandFonts();
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const color = accent === 'cyan' ? C.cyan : C.pink;
  const lines = title.split('\n');
  const longest = Math.max(...lines.map((l) => l.length));
  // Fit: Anton is ~0.5 em wide per glyph; keep inside 940 px.
  const size = Math.min(preset === 'neon' ? 200 : 180, Math.floor(940 / (longest * 0.52)));

  let words = 0;
  const headline = lines.map((line, li) => (
    <div key={li} style={{display: 'flex', justifyContent: 'center', gap: size * 0.22}}>
      {line.split(' ').map((word, wi) => {
        const i = words++;
        const start = 6 + i * (preset === 'punch' ? 5 : 3);
        const s = spring({frame: frame - start, fps, config: {damping: 14, stiffness: 160}});
        let style: React.CSSProperties = {};
        if (preset === 'punch') {
          style = {transform: `translateX(${(1 - s) * -900}px) skewX(${(1 - s) * -12}deg)`, color: C.cream,
            textShadow: '0 10px 30px rgba(0,0,0,.55)'};
        } else if (preset === 'ask') {
          style = {transform: `scale(${0.4 + 0.6 * s})`, opacity: s, color: C.cream,
            textShadow: '0 10px 30px rgba(0,0,0,.55)'};
        } else {
          const on = flicker(frame, start + 4);
          style = {opacity: 0.15 + 0.85 * on, color: '#fff3fa',
            textShadow: on > 0.5 ? neonGlow(color, 1.1) : 'none'};
        }
        return (
          <span key={wi} style={{display: 'inline-block', ...style}}>
            {word}
          </span>
        );
      })}
    </div>
  ));

  const subStart = 10 + words * 4;
  const subIn = spring({frame: frame - subStart, fps, config: {damping: 200}});
  const tagIn = interpolate(frame, [subStart + 10, subStart + 22], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const bob = Math.sin(frame / 6) * 14;

  return (
    <AbsoluteFill style={{backgroundColor: C.ink}}>
      <Background bg={bg} />
      <AbsoluteFill
        style={{
          background:
            'linear-gradient(180deg, rgba(8,4,18,.82) 0%, rgba(8,4,18,.45) 34%, rgba(8,4,18,0) 52%, rgba(8,4,18,0) 70%, rgba(8,4,18,.7) 100%)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          top: SAFE_TOP + (preset === 'ask' ? 40 : 110),
          left: 70,
          right: 70,
          fontFamily: 'Anton',
          fontSize: size,
          lineHeight: 1.04,
          textAlign: 'center',
          textTransform: 'uppercase',
        }}
      >
        {headline}
        {sub ? (
          <div
            style={{
              marginTop: 30,
              opacity: subIn,
              transform: `translateY(${(1 - subIn) * 40}px)`,
              fontFamily: scriptSub ? 'Pacifico' : 'Bebas Neue',
              fontSize: scriptSub ? 76 : 92,
              lineHeight: 1.2,
              textTransform: 'none',
              color: scriptSub ? color : C.cream,
              textShadow: scriptSub ? neonGlow(color, 0.35) : '0 6px 20px rgba(0,0,0,.6)',
            }}
          >
            {sub}
          </div>
        ) : null}
      </div>
      {preset === 'ask' ? (
        <div
          style={{
            position: 'absolute',
            top: 1010 + bob,
            left: '50%',
            width: 70,
            height: 70,
            marginLeft: -35,
            borderRight: `10px solid ${color}`,
            borderBottom: `10px solid ${color}`,
            transform: 'rotate(45deg)',
            opacity: tagIn,
            filter: `drop-shadow(0 0 14px ${color})`,
          }}
        />
      ) : null}
      <Tag opacity={tagIn} />
    </AbsoluteFill>
  );
};
