/**
 * SVG coordinate system utilities for timeline components
 */

// SVG viewBox dimensions
export const SVG_WIDTH = 1000
export const SVG_HEIGHT = 200
export const SVG_HEIGHT_BIFURCATING = 400

// Layout constants
export const PADDING_X = 100
export const LINE_Y = 50
export const TICK_RADIUS = 8
export const BRANCH_OFFSET_Y = 150

/**
 * Calculate X coordinate for a tick in the timeline
 * @param tickIndex - Index of the tick (0-based)
 * @param totalTicks - Total number of ticks
 * @returns X coordinate in SVG units
 */
export function getTickX(tickIndex: number, totalTicks: number): number {
  if (totalTicks === 1) return SVG_WIDTH / 2 // Center single tick

  const usableWidth = SVG_WIDTH - (PADDING_X * 2)
  return PADDING_X + (usableWidth * tickIndex / (totalTicks - 1))
}

/**
 * Get arrow head polygon points for timeline line
 * @returns Points string for SVG polygon
 */
export function getArrowPoints(): string {
  const arrowX = SVG_WIDTH - PADDING_X
  const arrowY = LINE_Y
  const arrowSize = 10

  return `${arrowX},${arrowY} ${arrowX - arrowSize},${arrowY - 6} ${arrowX - arrowSize},${arrowY + 6}`
}

/**
 * Calculate X coordinate for a branch tick
 * @param tickIndex - Index of the tick within the branch (0-based)
 * @param totalTicks - Total ticks in the branch
 * @param branchIdx - Index of the branch (0-based)
 * @returns X coordinate in SVG units
 */
export function getBranchTickX(tickIndex: number, totalTicks: number, branchIdx: number): number {
  // For branches, we use the same logic as main timeline ticks
  return getTickX(tickIndex, totalTicks)
}

/**
 * Calculate Y coordinate for a branch timeline
 * @param branchIdx - Index of the branch (0-based)
 * @returns Y coordinate in SVG units
 */
export function getBranchY(branchIdx: number): number {
  return LINE_Y + BRANCH_OFFSET_Y * (branchIdx + 1)
}

/**
 * Configuration for a connector line between main and branch timeline
 */
export interface ConnectorConfig {
  x1: number
  y1: number
  x2: number
  y2: number
}

/**
 * Calculate connector line configuration
 * @param mainTickIdx - Index of the main timeline tick where branch splits
 * @param mainTotalTicks - Total ticks in main timeline
 * @param branchTotalTicks - Total ticks in branch timeline
 * @param branchIdx - Index of the branch
 * @returns Connector line coordinates
 */
export function getConnectorConfig(
  mainTickIdx: number,
  mainTotalTicks: number,
  branchTotalTicks: number,
  branchIdx: number
): ConnectorConfig {
  const mainX = getTickX(mainTickIdx, mainTotalTicks)
  const branchX = getTickX(0, branchTotalTicks) // First tick of branch

  return {
    x1: mainX,
    y1: LINE_Y,
    x2: branchX,
    y2: getBranchY(branchIdx)
  }
}
