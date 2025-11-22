"use client";
import dynamic from 'next/dynamic';

const ForceGraph3D = dynamic(() => import('react-force-graph-3d'), {
  ssr: false
});

export default function Graph3D({ data }: { data: any }) {
  return (
    <ForceGraph3D
      graphData={data}
      nodeLabel="id"
      nodeColor={() => "#6366f1"} // Indigo color
      linkColor={() => "#ffffff"}
      linkOpacity={0.2}
      backgroundColor="#000000"
    />
  );
}
