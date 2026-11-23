// A 7-20 s Reel cut from monthly footage: hook text over the first shot
// (the first second decides the view), burned-in captions for sound-off
// viewers, and a neon end card that turns the view into a visit.
import React from 'react';
import {AbsoluteFill, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, SAFE_BOTTOM, SAFE_TOP, Tag, neonGlow, useBrandFonts} from './brand';

export type ReelClip = {src: string; seconds: number; startFrom?: number};
export type Caption = {text: string; from: number; to: number}; // seconds on the reel timeline
export type ReelProps = {clips: ReelClip[]; hook: string; captions?: Caption[]; cta?: string; endSeconds?: number};

const Hook: React.FC<{text: string}> = ({text}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 12, stiffness: 180}});
  const out = interpolate(frame, [2.2 * fps, 2.6 * fps], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', top: SAFE_TOP + 80, left: 60, right: 60, textAlign: 'center', opacity: out,
      transform: `scale(${0.6 + 0.4 * s})`, fontFamily: 'Anton', fontSize: 130, lineHeight: 1.04, color: C.cream,
      textTransform: 'uppercase', textShadow: '0 10px 34px rgba(0,0,0,.7)', whiteSpace: 'pre-line'}}>
      {text}
    </div>
  );
};

const Captions: React.FC<{captions: Caption[]}> = ({captions}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const c = captions.find((x) => t >= x.from && t < x.to);
  if (!c) return null;
  return (
    <div style={{position: 'absolute', bottom: SAFE_BOTTOM + 170, left: 80, right: 80, textAlign: 'center'}}>
      <span style={{fontFamily: 'Bebas Neue', fontSize: 78, lineHeight: 1.15, color: C.ink, background: C.cream,
        padding: '4px 18px', boxDecorationBreak: 'clone', WebkitBoxDecorationBreak: 'clone'}}>{c.text}</span>
    </div>
  );
};

const EndCard: React.FC<{cta: string}> = ({cta}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 16}});
  return (
    <AbsoluteFill style={{background: `radial-gradient(70% 45% at 50% 45%, ${C.pink}55, ${C.ink} 75%)`,
      alignItems: 'center', justifyContent: 'center', opacity: s}}>
      <div style={{fontFamily: 'Anton', fontSize: 210, lineHeight: 0.95, color: '#fff3fa', textAlign: 'center',
        textShadow: neonGlow(C.pink, 1.2), transform: `scale(${0.85 + 0.15 * s})`}}>BURGER<br />VIBES</div>
      <div style={{marginTop: 40, fontFamily: 'Pacifico', fontSize: 70, color: C.cyan, textShadow: neonGlow(C.cyan, 0.35)}}>{cta}</div>
      <Tag opacity={1} />
    </AbsoluteFill>
  );
};

export const Reel: React.FC<ReelProps> = ({clips, hook, captions = [], cta = 'Wir sehen uns!', endSeconds = 2.5}) => {
  useBrandFonts();
  const {fps} = useVideoConfig();
  let at = 0;
  const seqs = clips.map((c, i) => {
    const from = at;
    const len = Math.round(c.seconds * fps);
    at += len;
    return (
      <Sequence key={i} from={from} durationInFrames={len}>
        <OffthreadVideo src={staticFile(c.src)} startFrom={Math.round((c.startFrom ?? 0) * fps)} muted
          style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </Sequence>
    );
  });
  return (
    <AbsoluteFill style={{backgroundColor: C.ink}}>
      {seqs}
      <Sequence durationInFrames={Math.round(2.6 * fps)}>
        <Hook text={hook} />
      </Sequence>
      <Captions captions={captions} />
      <Sequence from={at} durationInFrames={Math.round(endSeconds * fps)}>
        <EndCard cta={cta} />
      </Sequence>
    </AbsoluteFill>
  );
};

export const reelFrames = (p: ReelProps, fps: number) =>
  p.clips.reduce((a, c) => a + Math.round(c.seconds * fps), 0) + Math.round((p.endSeconds ?? 2.5) * fps);
