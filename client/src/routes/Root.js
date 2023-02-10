import {MainButton} from "../components/Button";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";

const Center = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2em;
  width: 50%;
  margin: 8em auto;
  justify-content: center;
`

function Root() {
  const navigate = useNavigate();

  return(
    <Center>
      <MainButton onClick={() => navigate("/training")}>Training</MainButton>
      <MainButton onClick={() => navigate("/testing")}>Test</MainButton>
    </Center>
  )
}

export default Root;
