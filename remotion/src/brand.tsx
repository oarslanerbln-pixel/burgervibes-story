// Brand tokens and shared pieces for every Burger Vibes composition.
// Fonts come from assets/fonts (the Remotion public dir), never from a CDN:
// renders must work offline on the laptop and stay identical month to month.
import React, {useEffect, useState} from 'react';
import {continueRender, delayRender, staticFile} from 'remotion';

export const C = {
  ink: '#0d0717',
  pink: '#ff2d95',
  cyan: '#00e5ff',
  cream: '#fff4e6',
};
export const W = 1080;
export const H = 1920;
// Instagram covers the top ~250 px (progress bar, name) and the bottom
// ~340 px (reply bar). Everything readable lives between these lines.
export const SAFE_TOP = 250;
export const SAFE_BOTTOM = 340;

const FONTS: [string, string][] = [
  ['Anton', 'fonts/anton-latin.ttf'],
  ['Bebas Neue', 'fonts/bebas-neue-latin.ttf'],
  ['Pacifico', 'fonts/pacifico-latin.ttf'],
];

export const useBrandFonts = () => {
  const [handle] = useState(() => delayRender('brand fonts'));
  useEffect(() => {
    Promise.all(
      FONTS.map(([family, file]) => {
        const face = new FontFace(family, `url(${staticFile(file)})`);
        return face.load().then((f) => document.fonts.add(f));
      }),
    )
      .then(() => continueRender(handle))
      .catch((e) => {
        console.error(e);
        continueRender(handle);
      });
  }, [handle]);
};

export const neonGlow = (color: string, strength = 1) =>
  [
    `0 0 ${4 * strength}px #fff`,
    `0 0 ${10 * strength}px ${color}`,
    `0 0 ${24 * strength}px ${color}`,
    `0 0 ${48 * strength}px ${color}`,
    `0 0 ${90 * strength}px ${color}`,
  ].join(', ');

export const Tag: React.FC<{opacity: number; text?: string}> = ({opacity, text}) => (
  <div
    style={{
      position: 'absolute',
      left: '50%',
      bottom: SAFE_BOTTOM + 30,
      transform: 'translateX(-50%)',
      opacity,
      display: 'flex',
      alignItems: 'center',
      gap: 18,
      padding: '14px 34px 12px 26px',
      borderRadius: 999,
      border: `3px solid ${C.pink}`,
      background: 'rgba(10, 6, 24, 0.75)',
      fontFamily: 'Bebas Neue',
      fontSize: 46,
      color: C.cream,
      whiteSpace: 'nowrap',
    }}
  >
    <span style={{width: 18, height: 18, borderRadius: 9, background: C.cyan, boxShadow: neonGlow(C.cyan, 0.4)}} />
    {text ?? 'BURGER VIBES  ·  TEMPELHOFER DAMM 134'}
  </div>
);

export const isVideo = (src: string) => /\.(mp4|mov|m4v|webm)$/i.test(src);
