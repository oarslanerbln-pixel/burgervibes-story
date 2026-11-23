import React from 'react';
import {Composition} from 'remotion';
import {Story, StoryProps} from './Story';
import {Reel, ReelProps, reelFrames} from './Reel';
import {H, W} from './brand';

const FPS = 30;

export const Root: React.FC = () => (
  <>
    <Composition
      id="Story"
      component={Story}
      width={W}
      height={H}
      fps={FPS}
      durationInFrames={180}
      defaultProps={{title: 'FREITAG.\nNEON.\nBURGER.', sub: 'Heute Abend bei uns', scriptSub: true, preset: 'neon', accent: 'pink'} as StoryProps}
      calculateMetadata={({props}) => ({durationInFrames: Math.round((props.duration ?? 6) * FPS)})}
    />
    <Composition
      id="Reel"
      component={Reel}
      width={W}
      height={H}
      fps={FPS}
      durationInFrames={300}
      defaultProps={{
        clips: [{src: 'selects/W1-Mo-2.mp4', seconds: 3}, {src: 'selects/W1-Di-1.mp4', seconds: 3}],
        hook: 'WIE SCHNELL\nIST EIN BURGER?',
        captions: [{text: '100% Beef. 100% Halal.', from: 2.8, to: 5.8}],
        cta: 'Tempelhofer Damm 134',
      } as ReelProps}
      calculateMetadata={({props}) => ({durationInFrames: reelFrames(props, FPS)})}
    />
  </>
);
