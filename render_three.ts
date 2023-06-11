"use client";

import { useRef, useState, useEffect } from "react";
import { Canvas } from "@react-three/fiber";
import { CameraControls } from "@react-three/drei";

// const DisplayScreen = ({ pixelData }) => {
//   return (
//     <group position={[0, 0, 0]}>
//       <mesh>
//         <planeGeometry args={[1024, 1024]} />
//         <meshStandardMaterial color={"green"} />
//       </mesh>
//       {pixelData.map((row, rowIndex) => {
//         return row.map((pixelState, columnIndex) => {
//           return (
//             <mesh
//               position={[columnIndex, -rowIndex, pixelState < 0.8 ? 0 : pixelState * 5]}
//               key={`${rowIndex}-${columnIndex}`}
//               castShadow
//               receiveShadow
//             >
//               <boxGeometry args={[0.8, 0.8, 10]} />
//               <meshStandardMaterial
//                 color={pixelState < 0.8 ? "blue" : "red"}
//               />
//             </mesh>
//           );
//         });
//       })}
//     </group>
//   );
// };

const DisplayScreen = ({ frameData }) => {
  const gridSize = 128;

  // Creates the 3D pixel grid based on frameData's 2D arrays of 0s and 1s;
  const createPixelGrid = (data) => {
    const gridGeometry = new THREE.BufferGeometry();
    let positions = [];
    let colors = [];

    for (let i = 0; i < gridSize; i++) {
      for (let j = 0; j < gridSize; j++) {
        if (data[i][j] === 1) {
          positions.push(i - gridSize / 2, j - gridSize / 2, 0);

export default function ThreeCanvas() {
  const [allPixelData, setAllPixelData] = useState([]);
  const [pixelsSet, setPixelsSet] = useState(false); // TODO: use this to trigger animation
  const [currPixelData, setCurrPixelData] = useState([]);

  useEffect(() => {
    let pixelDataMap = new Map();

    Array.from({ length: 700 }, (x, i) => {
      const filePath = `/heart_depth_frames/${i}.json`;
      fetch(filePath)
        .then((res) => res.json())
        .then((data) => {
          pixelDataMap.set(i, data);
        })
        .catch((err) => console.log(err));
    });

    setAllPixelData(pixelDataMap);
    setPixelsSet(true);
  }, []);

  useEffect(() => {
    console.log("Starting animation");
    
    if (pixelsSet) {
      let currPixelDataIndex = 0;
      const interval = setInterval(() => {
        console.log(currPixelDataIndex);
        setCurrPixelData(allPixelData.get(currPixelDataIndex));
        currPixelDataIndex++;
        if (currPixelDataIndex === allPixelData.size) {
          currPixelDataIndex = 0;
        }
      }, 1000 / 30);
    }
  }, [pixelsSet]);

  return (
    <>
      <div className="h-screen w-screen">
        <Canvas camera={{ position: [0, 0, 10] }} shadows>
          <ambientLight />
          {/* <spotLight position={[0, 0, 100]} castShadow target-position={[0, 0, 0]} /> */}
          <directionalLight position={[0, 0, 100]} castShadow />
          <DisplayScreen pixelData={currPixelData} />
          <CameraControls />
        </Canvas>
      </div>
    </>
  );
}
