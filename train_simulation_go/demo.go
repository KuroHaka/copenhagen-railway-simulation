package main

import (
	"image/color"
	_ "image/png"
	"log"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
)

const (
	screenWidth  = 640
	screenHeight = 480
)

var mapImage *ebiten.Image
var train Train

// Simulation implements ebiten.Game interface.
type Element struct {
	posX  float64
	posY  float64
	image *ebiten.Image
}

func (t *Element) draw(screen *ebiten.Image) {
	op := &ebiten.DrawImageOptions{}
	op.GeoM.Translate(t.posX-(float64(t.image.Bounds().Dx())/2), t.posY-(float64(t.image.Bounds().Dy())/2))
	screen.DrawImage(t.image, op)
}

type Train struct {
	Element
	speed float32
}

type Simulation struct {
}

// Update proceeds the Simulation state.
// Update is called every tick (1/60 [s] by default not changable).
func (s *Simulation) Update() error {
	// Write your Simulation's logical update.
	return nil
}

// Draw draws the Simulation screen.
// Draw is called every frame (typically 1/60[s] for 60Hz display).
func (s *Simulation) Draw(screen *ebiten.Image) {
	// Write your Simulation's rendering.
	var err error
	mapImage, _, err = ebitenutil.NewImageFromFile("images/map.png")
	if err != nil {
		log.Fatal(err)
	}
	screen.DrawImage(mapImage, nil)
	train.posX += 1
	train.draw(screen)
}

// Layout takes the outside size (e.g., the window size) and returns the (logical) screen size.
// If you don't have to adjust the screen size with the outside size, just return a fixed size.
func (s *Simulation) Layout(outsideWidth, outsideHeight int) (screenWidth, screenHeight int) {
	return outsideWidth, outsideHeight
}

func main() {
	//Create objects
	trainImage := ebiten.NewImage(5, 5)
	trainImage.Fill(color.Black)
	train = Train{
		Element: Element{
			posX:  203,
			posY:  473,
			image: trainImage}}
	simulation := &Simulation{}
	// Specify the window size as you like. Here, a doubled size is specified.
	ebiten.SetWindowSize(1307, 979)
	ebiten.SetWindowTitle("The loop")
	ebiten.SetWindowResizable((true))
	// Call ebiten.RunGame to start your Simulation loop.
	if err := ebiten.RunGame(simulation); err != nil {
		log.Fatal(err)
	}
}
