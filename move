//
//  GameScene.swift
//  character
//
//  Created by 공사떼 on 2024/12/12.
//

import SpriteKit
import GameplayKit


class GameScene: SKScene {
    // 캐릭터 노드 선언
    var character: SKSpriteNode!

    
    override func didMove(to view: SKView) {
        print("GameScene loaded") // 확인용 메시지
        backgroundColor = .blue
        
        character = SKSpriteNode(imageNamed: "walk1")
        
        // 이미지 로드 상태 확인
        if character.texture == nil {
            print("Error: Image not found!") // 이미지 로드 실패 확인 메시지
        } else {
            print("Image loaded successfully!") // 이미지 로드 성공 메시지
        }
        character.position = CGPoint(x: size.width / 3, y: size.height / 3)
        character.anchorPoint = CGPoint(x: 0.5, y: 0.5) // 중앙 기준으로 배치
        character.size = CGSize(width: 300, height: 300)
        addChild(character)
        print("Character added to the scene")
        // 걷기 애니메이션 실행
        startWalkingAnimation()
        
        // 캐릭터 움직임 테스트
        moveCharacter(direction: "right", distance: 200, duration: 2)
        moveCharacter(direction: "up", distance: 200, duration: 2)
    }
    
   
    
    // 걷기 애니메이션 구현
    func startWalkingAnimation() {
        // 걷기 프레임 배열
        let walkTextures = [
            SKTexture(imageNamed: "walk1"),
            SKTexture(imageNamed: "walk2"),
            SKTexture(imageNamed: "walk3")
        ]
        
        // 애니메이션 액션
        let walkAnimation = SKAction.animate(with: walkTextures, timePerFrame: 0.1)
        let repeatWalk = SKAction.repeatForever(walkAnimation)
        
        // 캐릭터에 애니메이션 실행
        character.run(repeatWalk)
    }
    
    // 캐릭터 이동 구현
    func moveCharacter(direction: String, distance: CGFloat, duration: TimeInterval) {
        var moveAction: SKAction!
        
        if direction == "right" {
            // 오른쪽 이동 액션
            moveAction = SKAction.moveBy(x: distance, y: 0, duration: duration)
            character.xScale = 1 // 방향 유지
        } else if direction == "left" {
            // 왼쪽 이동 액션
            moveAction = SKAction.moveBy(x: -distance, y: 0, duration: duration)
            character.xScale = -1 // 캐릭터 반전
        }
        
        if direction == "up" {
            // 오른쪽 이동 액션
            moveAction = SKAction.moveBy(x: 0, y: distance, duration: duration)
            character.yScale = 1 // 방향 유지
        } else if direction == "down" {
            // 왼쪽 이동 액션
            moveAction = SKAction.moveBy(x: 0, y: -distance, duration: duration)
            character.yScale = -1 // 캐릭터 반전
        }
        
        // 이동 액션 실행
        character.run(moveAction)
    }
    
    // 터치 이벤트로 이동 제어
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        guard let touch = touches.first else { return }
        let location = touch.location(in: self)
        
        // 터치한 위치에 따라 이동 방향 설정
        if location.x > character.position.x {
            moveCharacter(direction: "right", distance: 200, duration: 2)
        } else {
            moveCharacter(direction: "left", distance: 200, duration: 2)
        }
        
        if location.y > character.position.y {
            moveCharacter(direction: "up", distance: 200, duration: 2)
        } else {
            moveCharacter(direction: "down", distance: 200, duration: 2)
        }
    }
}
