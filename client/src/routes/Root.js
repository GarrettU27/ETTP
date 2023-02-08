import {MainButton} from "../components/Button";
import styled from "styled-components";

const Center = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2em;
  width: 50%;
  margin: 8em auto;
  justify-content: center;
`

function Root() {
  return(
    <Center>
      <MainButton>Training</MainButton>
      <MainButton>Test</MainButton>
    </Center>
  )
}

export default Root;
