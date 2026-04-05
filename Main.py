import cv2
import numpy as np

# Load image
image = cv2.imread("Screenshot 2026-03-25 182744 (1).png")
output = image.copy()

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (9, 9), 2)

# Detect circles
circles = cv2.HoughCircles(
    gray,
    cv2.HOUGH_GRADIENT,
    dp=1,
    minDist=50,
    param1=50,
    param2=30,
    minRadius=10,
    maxRadius=100
)

errors = []
score = 100

if circles is not None:
    circles = np.uint16(np.around(circles))

    for i in circles[0, :]:
        cv2.circle(output, (i[0], i[1]), i[2], (0, 255, 0), 2)

    # Check spacing
    for i in range(len(circles[0])):
        for j in range(i + 1, len(circles[0])):

            x1, y1, r1 = map(int, circles[0][i])
            x2, y2, r2 = map(int, circles[0][j])

            distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

            if distance < 1.5 * max(r1, r2):
                errors.append("Holes too close")
                score -= 30

                cv2.line(output, (x1, y1), (x2, y2), (0, 0, 255), 2)

else:
    errors.append("No holes detected")
    score -= 20

print("\n=== DESIGN VALIDATION REPORT ===")

if errors:
    for e in errors:
        print(e)
else:
    print("Design is OK")

print(f"\nDesign Score: {score}/100")

cv2.imshow("Validation Result", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
